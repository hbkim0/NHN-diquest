import collections
import dataclasses
import pathlib

import yaml
import fastjsonschema

from . import const
from . import config

import logging
from typing import Mapping, Iterable, Callable


@dataclasses.dataclass
class _SchemaFile():
    datasets: Iterable[pathlib.Path] = tuple()
    collection: pathlib.Path = pathlib.Path()


_SCHEMA_FILES = collections.defaultdict(pathlib.Path, {
    const.SupportedDatasetType.VERSIONED_IMAGE_TAGGING: _SchemaFile(
        [pathlib.Path(config.SCHEMA_BASE_PATH, 'k-fashion-dataset.schema.yaml')],
    ),
    const.SupportedDatasetType.DATASET_IMAGE_TAGGING: _SchemaFile(
        [pathlib.Path(config.SCHEMA_BASE_PATH, 'k-fashion-dataset.schema.yaml')],
    ),
})


_schemas: Mapping[pathlib.Path, str] = dict()
_validate_functions: Mapping[const.SupportedDatasetType, Iterable[Callable]] = dict()
_logger = logging.getLogger(__name__)


def _get_schema_string(path: pathlib.Path) -> str:

    #
    schemas = _schemas

    #
    if path not in schemas:
        s = ''
        if path.is_file():
            with open(path, 'r') as fin:
                s = fin.read()

        schemas[path] = s

    return schemas[path]


def validate_dataset(dataset_type: const.SupportedDatasetType, doc: Mapping) -> bool:

    #
    validate_functions = _validate_functions

    #
    if dataset_type not in validate_functions:
        functions = []
        for schema_file in _SCHEMA_FILES[dataset_type].datasets:
            #
            schema_string = _get_schema_string(schema_file)

            #
            schema_obj = yaml.full_load(schema_string)

            #
            functions.append(fastjsonschema.compile(schema_obj))

        #
        validate_functions[dataset_type] = functions
    functions = validate_functions[dataset_type]

    #
    is_valid = False
    for f in functions:
        try:
            f(doc)
        except fastjsonschema.JsonSchemaValueException as e:
            _logger.debug(f'invalid annotation: {e}')
        else:
            is_valid = True
            break

    return is_valid


def get_info_schema(dataset_type: const.SupportedDatasetType) -> str:

    #
    schema_file = _SCHEMA_FILES[dataset_type].collection

    return _get_schema_string(schema_file)
