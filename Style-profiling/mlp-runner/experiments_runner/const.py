# import uuid

# # see:
# #  - ingestor/ingestor/const.py:SupportedDatasetType
# #  - ingestor/ingestor/const.py:RESOUECE_URL
# RESOURCE_URL_DATASET = 'ai-dev.diquest.com/resources/datasets/{dataset_name}/version/{version}'

# # see:
# #  - models/registerer/database.py:ModelDatabase.upsert
# #  - models/registerer/model_register.py:yolov5
# #  - models/registerer/model_register.py:cp_vton
# #  - models/registerer/model_register.py:image_tagging_classifier
# RESOURCE_URL_MODEL = 'ai-dev.diquest.com/resources/models/{model_name}'


# def RESOURCE_ID_DATASET(dataset_name: str, version: str = 'v1.0') -> str:
#     return str(uuid.uuid3(uuid.NAMESPACE_URL, RESOURCE_URL_DATASET.format(dataset_name=dataset_name, version=version)))


# def RESOURCE_ID_MODEL(model_name: str) -> str:
#     return str(uuid.uuid3(uuid.NAMESPACE_URL, RESOURCE_URL_MODEL.format(model_name=model_name)))
