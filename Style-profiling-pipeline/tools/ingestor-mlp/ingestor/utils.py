import dataclasses
import shutil
import uuid
import pathlib

from . import const
from . import config

from typing import Optional, Union


@dataclasses.dataclass(repr=False)
class DatasetCount():
    description: str = ''

    data: int = 0

    def __repr__(self):
        return '{:-^80}\n'.format(f' {self.description} counts ') + \
               f'dataset : {self.data}' 

    def increase(self):
        self.data += 1


@dataclasses.dataclass(repr=False)
class DatasetCountVersioned():
    description: str = ''

    training: int = 0
    validation: int = 0
    none: int = 0

    def __repr__(self):
        return '{:-^80}\n'.format(f' {self.description} counts ') + \
               f'Training : {self.training} | Validation : {self.validation} | None : {self.none}'

    def increase(self, purpose: str = 'none') -> None:
        if purpose == 'training':
            self.training += 1
        elif purpose == 'validation':
            self.validation += 1
        elif purpose == 'none':
            self.none += 1

    def as_dict(self) -> dict:
        return {'training': self.training, 'validation': self.validation, 'none': self.none}


def _get_resource_id(l1: str, l2: str, l3: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, const.RESOUECE_URL.format(l1=l1, l2=l2, l3=l3)))


def get_resource_id_dataset(dataset_type: const.SupportedDatasetType, version: str = 'v1.0') -> str:
    return _get_resource_id(dataset_type.value, 'version', version)


def get_resource_id_example(dataset_type: const.SupportedDatasetType, _example_id: str) -> str:
    return _get_resource_id(dataset_type.value, 'example', _example_id)


def get_resource_id_feature(dataset_type: const.SupportedDatasetType, feature_type: str, feature_id: str) -> str:
    return _get_resource_id(dataset_type.value, feature_type, feature_id)


def copy_file(
    dataset_id: str,
    dataset_type: const.SupportedDatasetType,
    feature_type: str,
    feature_id: str,
    src_path: Union[str, pathlib.Path],
    exist_ok: bool = False
) -> Optional[str]:

    #
    src_path = pathlib.Path(src_path)
    if not src_path.is_file():
        raise ValueError(f'"{src_path}" not found')

    #
    dst = pathlib.Path(
        get_resource_id_feature(dataset_type, feature_type, feature_id)
    ).with_suffix(src_path.suffix)

    #
    dst_path = pathlib.Path(config.FS_BASE_PATH, dataset_id, dst)
    if dst_path.exists():
        return str(dst) if exist_ok else None

    #
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_bytes(
        src_path.read_bytes()
    )

    return str(dst)


def remove_file(file: Union[str, pathlib.Path]) -> None:
    #
    file = pathlib.Path(config.FS_BASE_PATH, file)

    #
    return file.unlink(missing_ok=True)


def clean_files() -> None:
    shutil.rmtree(config.FS_BASE_PATH, ignore_errors=True)
