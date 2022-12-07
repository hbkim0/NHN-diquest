import enum


class SupportedDatasetType(enum.Enum):
    RECOMMENDATION = 'recommend-dataset'

class SupportedCollection(enum.Enum):
    PRODUCT = 'products'
    CUSTOMER = 'customers'
    HISTORY = 'historys'


