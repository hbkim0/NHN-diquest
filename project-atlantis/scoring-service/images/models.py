from typing import Iterable, List
from gridfs import NoFile

from django.core.files import File
from djongo.storage import GridFSStorage


class ImageFSStorage(GridFSStorage):
    MEDIA_ROOT = 'images'

    def __init__(self, location='', collection='fs', database='default', base_url=None):
        super().__init__(location=location, collection=collection, database=database, base_url=base_url)

    def _get_gridfs(self, path):
        '''djongo에서 db connection을 어떻게 관리하는지 잘 모르겠음.
        connection이 없을 경우 connect하게 workaround code 추가
        '''

        if not hasattr(self, '_db'):
            from django.db import connections
            if connections[self.database].connection is None:
                connections[self.database].connect()

        return super()._get_gridfs(path)

    def save_images(self, images: Iterable[File]) -> List[str]:
        return [self.save(f'{ImageFSStorage.MEDIA_ROOT}/{image.name}', image) for image in images]

    def open_image(self, filename: str) -> File:

        if not filename.startswith(f'{ImageFSStorage.MEDIA_ROOT}/'):
            filename = f'{ImageFSStorage.MEDIA_ROOT}/{filename}'

        try:
            file = self.open(filename)
        except NoFile:
            raise FileNotFoundError

        return file
