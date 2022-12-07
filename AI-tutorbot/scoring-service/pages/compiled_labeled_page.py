VERSION = "2.16.1"
from fastjsonschema import JsonSchemaValueException


NoneType = type(None)

def validate(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (dict)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be object", value=data, name="" + (name_prefix or "data") + "", definition={'$id': 'http://ai-dev.diquest.com/labeled-page.schema.yaml', '$schema': 'http://json-schema.org/draft-07/schema#', 'title': 'labeled page schema', 'type': 'object', 'required': ['width', 'height', 'vector', 'problems'], 'properties': {'width': {'type': 'integer', 'minimum': 1}, 'height': {'type': 'integer', 'minimum': 1}, 'vector': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 512, 'maxItems': 512}, 'problems': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}}}}, rule='type')
    data_is_dict = isinstance(data, dict)
    if data_is_dict:
        data_len = len(data)
        if not all(prop in data for prop in ['width', 'height', 'vector', 'problems']):
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must contain ['width', 'height', 'vector', 'problems'] properties", value=data, name="" + (name_prefix or "data") + "", definition={'$id': 'http://ai-dev.diquest.com/labeled-page.schema.yaml', '$schema': 'http://json-schema.org/draft-07/schema#', 'title': 'labeled page schema', 'type': 'object', 'required': ['width', 'height', 'vector', 'problems'], 'properties': {'width': {'type': 'integer', 'minimum': 1}, 'height': {'type': 'integer', 'minimum': 1}, 'vector': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 512, 'maxItems': 512}, 'problems': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}}}}, rule='required')
        data_keys = set(data.keys())
        if "width" in data_keys:
            data_keys.remove("width")
            data__width = data["width"]
            if not isinstance(data__width, (int)) and not (isinstance(data__width, float) and data__width.is_integer()) or isinstance(data__width, bool):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".width must be integer", value=data__width, name="" + (name_prefix or "data") + ".width", definition={'type': 'integer', 'minimum': 1}, rule='type')
            if isinstance(data__width, (int, float)):
                if data__width < 1:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".width must be bigger than or equal to 1", value=data__width, name="" + (name_prefix or "data") + ".width", definition={'type': 'integer', 'minimum': 1}, rule='minimum')
        if "height" in data_keys:
            data_keys.remove("height")
            data__height = data["height"]
            if not isinstance(data__height, (int)) and not (isinstance(data__height, float) and data__height.is_integer()) or isinstance(data__height, bool):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".height must be integer", value=data__height, name="" + (name_prefix or "data") + ".height", definition={'type': 'integer', 'minimum': 1}, rule='type')
            if isinstance(data__height, (int, float)):
                if data__height < 1:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".height must be bigger than or equal to 1", value=data__height, name="" + (name_prefix or "data") + ".height", definition={'type': 'integer', 'minimum': 1}, rule='minimum')
        if "vector" in data_keys:
            data_keys.remove("vector")
            data__vector = data["vector"]
            if not isinstance(data__vector, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".vector must be array", value=data__vector, name="" + (name_prefix or "data") + ".vector", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 512, 'maxItems': 512}, rule='type')
            data__vector_is_list = isinstance(data__vector, (list, tuple))
            if data__vector_is_list:
                data__vector_len = len(data__vector)
                if data__vector_len < 512:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".vector must contain at least 512 items", value=data__vector, name="" + (name_prefix or "data") + ".vector", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 512, 'maxItems': 512}, rule='minItems')
                if data__vector_len > 512:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".vector must contain less than or equal to 512 items", value=data__vector, name="" + (name_prefix or "data") + ".vector", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 512, 'maxItems': 512}, rule='maxItems')
                for data__vector_x, data__vector_item in enumerate(data__vector):
                    if not isinstance(data__vector_item, (int, float)) or isinstance(data__vector_item, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".vector[{data__vector_x}]".format(**locals()) + " must be number", value=data__vector_item, name="" + (name_prefix or "data") + ".vector[{data__vector_x}]".format(**locals()) + "", definition={'type': 'number'}, rule='type')
        if "problems" in data_keys:
            data_keys.remove("problems")
            data__problems = data["problems"]
            if not isinstance(data__problems, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems must be array", value=data__problems, name="" + (name_prefix or "data") + ".problems", definition={'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}}, rule='type')
            data__problems_is_list = isinstance(data__problems, (list, tuple))
            if data__problems_is_list:
                data__problems_len = len(data__problems)
                if data__problems_len < 1:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems must contain at least 1 items", value=data__problems, name="" + (name_prefix or "data") + ".problems", definition={'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}}, rule='minItems')
                for data__problems_x, data__problems_item in enumerate(data__problems):
                    if not isinstance(data__problems_item, (dict)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}]".format(**locals()) + " must be object", value=data__problems_item, name="" + (name_prefix or "data") + ".problems[{data__problems_x}]".format(**locals()) + "", definition={'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}, rule='type')
                    data__problems_item_is_dict = isinstance(data__problems_item, dict)
                    if data__problems_item_is_dict:
                        data__problems_item_len = len(data__problems_item)
                        if not all(prop in data__problems_item for prop in ['prob_num', 'solving_url', 'similar_url', 'labels']):
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}]".format(**locals()) + " must contain ['prob_num', 'solving_url', 'similar_url', 'labels'] properties", value=data__problems_item, name="" + (name_prefix or "data") + ".problems[{data__problems_x}]".format(**locals()) + "", definition={'type': 'object', 'required': ['prob_num', 'solving_url', 'similar_url', 'labels'], 'properties': {'prob_num': {'type': 'string'}, 'solving_url': {'type': 'string'}, 'similar_url': {'type': 'string'}, 'labels': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}}}, rule='required')
                        data__problems_item_keys = set(data__problems_item.keys())
                        if "prob_num" in data__problems_item_keys:
                            data__problems_item_keys.remove("prob_num")
                            data__problems_item__probnum = data__problems_item["prob_num"]
                            if not isinstance(data__problems_item__probnum, (str)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].prob_num".format(**locals()) + " must be string", value=data__problems_item__probnum, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].prob_num".format(**locals()) + "", definition={'type': 'string'}, rule='type')
                        if "solving_url" in data__problems_item_keys:
                            data__problems_item_keys.remove("solving_url")
                            data__problems_item__solvingurl = data__problems_item["solving_url"]
                            if not isinstance(data__problems_item__solvingurl, (str)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].solving_url".format(**locals()) + " must be string", value=data__problems_item__solvingurl, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].solving_url".format(**locals()) + "", definition={'type': 'string'}, rule='type')
                        if "similar_url" in data__problems_item_keys:
                            data__problems_item_keys.remove("similar_url")
                            data__problems_item__similarurl = data__problems_item["similar_url"]
                            if not isinstance(data__problems_item__similarurl, (str)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].similar_url".format(**locals()) + " must be string", value=data__problems_item__similarurl, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].similar_url".format(**locals()) + "", definition={'type': 'string'}, rule='type')
                        if "labels" in data__problems_item_keys:
                            data__problems_item_keys.remove("labels")
                            data__problems_item__labels = data__problems_item["labels"]
                            if not isinstance(data__problems_item__labels, (list, tuple)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels".format(**locals()) + " must be array", value=data__problems_item__labels, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels".format(**locals()) + "", definition={'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}, rule='type')
                            data__problems_item__labels_is_list = isinstance(data__problems_item__labels, (list, tuple))
                            if data__problems_item__labels_is_list:
                                data__problems_item__labels_len = len(data__problems_item__labels)
                                if data__problems_item__labels_len < 1:
                                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels".format(**locals()) + " must contain at least 1 items", value=data__problems_item__labels, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels".format(**locals()) + "", definition={'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}}, rule='minItems')
                                for data__problems_item__labels_x, data__problems_item__labels_item in enumerate(data__problems_item__labels):
                                    if not isinstance(data__problems_item__labels_item, (dict)):
                                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}]".format(**locals()) + " must be object", value=data__problems_item__labels_item, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}]".format(**locals()) + "", definition={'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}, rule='type')
                                    data__problems_item__labels_item_is_dict = isinstance(data__problems_item__labels_item, dict)
                                    if data__problems_item__labels_item_is_dict:
                                        data__problems_item__labels_item_len = len(data__problems_item__labels_item)
                                        if not all(prop in data__problems_item__labels_item for prop in ['bbox', 'label']):
                                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}]".format(**locals()) + " must contain ['bbox', 'label'] properties", value=data__problems_item__labels_item, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}]".format(**locals()) + "", definition={'type': 'object', 'required': ['bbox', 'label'], 'properties': {'bbox': {'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, 'label': {'type': 'string'}}}, rule='required')
                                        data__problems_item__labels_item_keys = set(data__problems_item__labels_item.keys())
                                        if "bbox" in data__problems_item__labels_item_keys:
                                            data__problems_item__labels_item_keys.remove("bbox")
                                            data__problems_item__labels_item__bbox = data__problems_item__labels_item["bbox"]
                                            if not isinstance(data__problems_item__labels_item__bbox, (list, tuple)):
                                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + " must be array", value=data__problems_item__labels_item__bbox, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='type')
                                            data__problems_item__labels_item__bbox_is_list = isinstance(data__problems_item__labels_item__bbox, (list, tuple))
                                            if data__problems_item__labels_item__bbox_is_list:
                                                data__problems_item__labels_item__bbox_len = len(data__problems_item__labels_item__bbox)
                                                if data__problems_item__labels_item__bbox_len < 4:
                                                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + " must contain at least 4 items", value=data__problems_item__labels_item__bbox, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='minItems')
                                                if data__problems_item__labels_item__bbox_len > 4:
                                                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + " must contain less than or equal to 4 items", value=data__problems_item__labels_item__bbox, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox".format(**locals()) + "", definition={'type': 'array', 'items': {'type': 'number'}, 'minItems': 4, 'maxItems': 4}, rule='maxItems')
                                                for data__problems_item__labels_item__bbox_x, data__problems_item__labels_item__bbox_item in enumerate(data__problems_item__labels_item__bbox):
                                                    if not isinstance(data__problems_item__labels_item__bbox_item, (int, float)) or isinstance(data__problems_item__labels_item__bbox_item, bool):
                                                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox[{data__problems_item__labels_item__bbox_x}]".format(**locals()) + " must be number", value=data__problems_item__labels_item__bbox_item, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].bbox[{data__problems_item__labels_item__bbox_x}]".format(**locals()) + "", definition={'type': 'number'}, rule='type')
                                        if "label" in data__problems_item__labels_item_keys:
                                            data__problems_item__labels_item_keys.remove("label")
                                            data__problems_item__labels_item__label = data__problems_item__labels_item["label"]
                                            if not isinstance(data__problems_item__labels_item__label, (str)):
                                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].label".format(**locals()) + " must be string", value=data__problems_item__labels_item__label, name="" + (name_prefix or "data") + ".problems[{data__problems_x}].labels[{data__problems_item__labels_x}].label".format(**locals()) + "", definition={'type': 'string'}, rule='type')
    return data