from rest_framework.decorators import api_view

from django.http import FileResponse
from misc.response import *

from .models import ImageFSStorage

_storage = ImageFSStorage()


@api_view(['POST', ])
def upload_images(request):
    paths = _storage.save_images(request.FILES.getlist('images', []))
    return ResponseOK({'paths': paths})


@api_view(['GET', ])
def download_image(request, filename):
    try:
        file = _storage.open_image(filename)
    except FileNotFoundError:
        return ResponseError404NotFound(0, f'not found: {filename}')

    return FileResponse(file, as_attachment=False)
