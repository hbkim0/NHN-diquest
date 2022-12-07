import logging
import os
import io
import base64
import json
from PIL import Image
from captum.attr import IntegratedGradients
import torch
from torchvision import transforms
from ts.torch_handler.base_handler import BaseHandler


logger = logging.getLogger(__name__)

ipex_enabled = False
if os.environ.get("TS_IPEX_ENABLE", "false") == "true":
    try:
        import intel_extension_for_pytorch as ipex
        ipex_enabled = True
    except ImportError as error:
        logger.warning("IPEX is enabled but intel-extension-for-pytorch is not installed. Proceeding without IPEX.")

class TaggingHandler(BaseHandler):

    _img_size = [224, 224]
    threshold = 0.0
    topk = 20
    image_processing = transforms.Compose([
        transforms.Resize(_img_size),
        transforms.ToTensor(), 
        transforms.Normalize(
            [0.485, 0.456, 0.406], 
            [0.229, 0.224, 0.225])
    ])

    def initialize(self, context):
        properties = context.system_properties
        self.map_location = "cuda" if torch.cuda.is_available(
        ) and properties.get("gpu_id") is not None else "cpu"
        self.device = torch.device(
            self.map_location + ":" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else self.map_location
        )
        self.manifest = context.manifest

        model_dir = properties.get("model_dir")
        model_pt_path = None
        if "serializedFile" in self.manifest["model"]:
            serialized_file = self.manifest["model"]["serializedFile"]
            model_pt_path = os.path.join(model_dir, serialized_file)

        # model def file
        model_file = self.manifest["model"].get("modelFile", "")

        if model_file:
            logger.debug("Loading eager model")
            self.model = self._load_pickled_model(
                model_dir, model_file, model_pt_path)
            self.model.to(self.device)
        else:
            logger.debug("Loading torchscript model")
            if not os.path.isfile(model_pt_path):
                raise RuntimeError("Missing the model.pt file")

            self.model = self._load_torchscript_model(model_pt_path)

        self.model.eval()
        if ipex_enabled:
            self.model = self.model.to(memory_format=torch.channels_last)
            self.model = ipex.optimize(self.model)

        logger.debug('Model file %s loaded successfully', model_pt_path)

        # Load class mapping for classifiers
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")
        self.mapping = self._load_label_mapping(mapping_file_path)

        self.ig = IntegratedGradients(self.model)
        self.initialized = True
        properties = context.system_properties
        if not properties.get("limit_max_image_pixels"):
            Image.MAX_IMAGE_PIXELS = None

    def preprocess(self, data):
        images = []

        for row in data:
            # Compat layer: normally the envelope should just return the data
            # directly, but older versions of Torchserve didn't have envelope.
            image = row.get("data") or row.get("body")
            if isinstance(image, str):
                # if the image is a string of bytesarray.
                image = base64.b64decode(image)

            # If the image is sent as bytesarray
            if isinstance(image, (bytearray, bytes)):
                image = Image.open(io.BytesIO(image))
                image = self.image_processing(image)
            else:
                # if the image is a list
                image = torch.FloatTensor(image)

            images.append(image)

        return torch.stack(images).to(self.device)

    def postprocess(self, data):
        probs, classes = torch.topk(data, self.topk)
        probs = probs.tolist()[0]
        classes = classes.tolist()[0]

        filtered_classes = [{'index': c, 'prob': p} for p,c in zip(probs, classes) if p >= self.threshold]
        if self.mapping:
            for item in filtered_classes:
                item['class'] = self.mapping[str(item['index'])]
        return [filtered_classes]

    def _load_label_mapping(self, mapping_file_path):
        if not os.path.isfile(mapping_file_path):
            logger.warning('Missing the index_to_name.json file. Inference output will not include class name.')
            return None
        with open(mapping_file_path, encoding="utf-8") as f:
            mapping = json.load(f)

        if not isinstance(mapping, dict):
            raise Exception('index_to_name mapping should be in "class":"label" json format')

        for key, value in mapping.items():
            new_value = value
            if not isinstance(new_value, str):
                raise Exception('labels in index_to_name must be either str')
            mapping[key] = new_value

        return mapping
