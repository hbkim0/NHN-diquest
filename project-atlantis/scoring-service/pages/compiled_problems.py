VERSION = "2.16.1"
from fastjsonschema import JsonSchemaValueException


NoneType = type(None)

def validate(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (list, tuple)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be array", value=data, name="" + (name_prefix or "data") + "", definition={'$id': 'http://ai-dev.diquest.com/problems.schema.yaml', '$schema': 'http://json-schema.org/draft-07/schema#', 'title': 'problems schema', 'type': 'array', 'items': {'type': 'object', 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string', 'description': '문제풀이 이미지 url'}, 'similar_url': {'type': 'string', 'description': '유사문제 이미지 url'}, 'labels': {'type': 'array', 'items': {'type': 'object', 'properties': {'bbox': {'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}}, rule='type')
    data_is_list = isinstance(data, (list, tuple))
    if data_is_list:
        data_len = len(data)
        for data_x, data_item in enumerate(data):
            if not isinstance(data_item, (dict)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}]".format(**locals()) + " must be object", value=data_item, name="" + (name_prefix or "data") + "[{data_x}]".format(**locals()) + "", definition={'type': 'object', 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string', 'description': '문제풀이 이미지 url'}, 'similar_url': {'type': 'string', 'description': '유사문제 이미지 url'}, 'labels': {'type': 'array', 'items': {'type': 'object', 'properties': {'bbox': {'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}, rule='type')
            data_item_is_dict = isinstance(data_item, dict)
            if data_item_is_dict:
                data_item_keys = set(data_item.keys())
                if "prob_num" in data_item_keys:
                    data_item_keys.remove("prob_num")
                    data_item__probnum = data_item["prob_num"]
                    if not isinstance(data_item__probnum, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].prob_num".format(**locals()) + " must be string", value=data_item__probnum, name="" + (name_prefix or "data") + "[{data_x}].prob_num".format(**locals()) + "", definition={'type': 'string'}, rule='type')
                if "solving_url" in data_item_keys:
                    data_item_keys.remove("solving_url")
                    data_item__solvingurl = data_item["solving_url"]
                    if not isinstance(data_item__solvingurl, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].solving_url".format(**locals()) + " must be string", value=data_item__solvingurl, name="" + (name_prefix or "data") + "[{data_x}].solving_url".format(**locals()) + "", definition={'type': 'string', 'description': '문제풀이 이미지 url'}, rule='type')
                if "similar_url" in data_item_keys:
                    data_item_keys.remove("similar_url")
                    data_item__similarurl = data_item["similar_url"]
                    if not isinstance(data_item__similarurl, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].similar_url".format(**locals()) + " must be string", value=data_item__similarurl, name="" + (name_prefix or "data") + "[{data_x}].similar_url".format(**locals()) + "", definition={'type': 'string', 'description': '유사문제 이미지 url'}, rule='type')
                if "labels" in data_item_keys:
                    data_item_keys.remove("labels")
                    data_item__labels = data_item["labels"]
                    if not isinstance(data_item__labels, (list, tuple)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels".format(**locals()) + " must be array", value=data_item__labels, name="" + (name_prefix or "data") + "[{data_x}].labels".format(**locals()) + "", definition={'type': 'array', 'items': {'type': 'object', 'properties': {'bbox': {'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}, rule='type')
                    data_item__labels_is_list = isinstance(data_item__labels, (list, tuple))
                    if data_item__labels_is_list:
                        data_item__labels_len = len(data_item__labels)
                        for data_item__labels_x, data_item__labels_item in enumerate(data_item__labels):
                            if not isinstance(data_item__labels_item, (dict)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}]".format(**locals()) + " must be object", value=data_item__labels_item, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}]".format(**locals()) + "", definition={'type': 'object', 'properties': {'bbox': {'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}, rule='type')
                            data_item__labels_item_is_dict = isinstance(data_item__labels_item, dict)
                            if data_item__labels_item_is_dict:
                                data_item__labels_item_keys = set(data_item__labels_item.keys())
                                if "bbox" in data_item__labels_item_keys:
                                    data_item__labels_item_keys.remove("bbox")
                                    data_item__labels_item__bbox = data_item__labels_item["bbox"]
                                    if not isinstance(data_item__labels_item__bbox, (list, tuple)):
                                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + " must be array", value=data_item__labels_item__bbox, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='type')
                                    data_item__labels_item__bbox_is_list = isinstance(data_item__labels_item__bbox, (list, tuple))
                                    if data_item__labels_item__bbox_is_list:
                                        data_item__labels_item__bbox_len = len(data_item__labels_item__bbox)
                                        if data_item__labels_item__bbox_len < 4:
                                            raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + " must contain at least 4 items", value=data_item__labels_item__bbox, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='minItems')
                                        if data_item__labels_item__bbox_len > 4:
                                            raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + " must contain less than or equal to 4 items", value=data_item__labels_item__bbox, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'description': '[left, top, right, bottom]', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='maxItems')
                                        for data_item__labels_item__bbox_x, data_item__labels_item__bbox_item in enumerate(data_item__labels_item__bbox):
                                            if not isinstance(data_item__labels_item__bbox_item, (int, float)) or isinstance(data_item__labels_item__bbox_item, bool):
                                                raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox[{data_item__labels_item__bbox_x}]".format(**locals()) + " must be number", value=data_item__labels_item__bbox_item, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].bbox[{data_item__labels_item__bbox_x}]".format(**locals()) + "", definition={'type': 'number'}, rule='type')
                                if "label" in data_item__labels_item_keys:
                                    data_item__labels_item_keys.remove("label")
                                    data_item__labels_item__label = data_item__labels_item["label"]
                                    if not isinstance(data_item__labels_item__label, (str)):
                                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].label".format(**locals()) + " must be string", value=data_item__labels_item__label, name="" + (name_prefix or "data") + "[{data_x}].labels[{data_item__labels_x}].label".format(**locals()) + "", definition={'type': 'string'}, rule='type')
    return data