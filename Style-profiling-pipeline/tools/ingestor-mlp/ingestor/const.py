import enum


class SupportedDatasetType(enum.Enum):
    VERSIONED_IMAGE_TAGGING = 'versioned-image-tagging'
    VERSIONED_TEXT_TAGGING = 'versioned-text-tagging'
    DATASET_IMAGE_TAGGING = 'dataset-image-tagging'
    DATASET_TEXT_TAGGING = 'dataset-text-tagging'

class SupportedCollection(enum.Enum):
    FILE = 'files'
    ANNOTATION = 'annotations'
    LABELS = 'labels'
    BUNDLES = 'bundles'
    DATASETS = 'datasets'
    VERSIONED_DATASET = 'versioned_dataset'

class SupportedMltask(enum.Enum):
    TEXT_TAGGING = 0
    IMAGE_TAGGING = 1
    

#
RESOUECE_URL = 'ai-dev.diquest.com/resources/files/{l1}/{l2}/{l3}'
