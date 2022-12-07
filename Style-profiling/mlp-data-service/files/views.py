import datetime
import urllib.parse
import bson
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from misc.response import *
from misc import query_string

from .serializers import FileSerializer, FileUploadSerializer
from .models import File
from annotations.serializers import AnnotationCreateDtoSerializer
from datasets.models import Dataset

class FileList(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        dataset_id = request.POST.get('dataset_id', '')
        bundle_id = request.POST.get('bundle_id', '')
        files = request.FILES.getlist('files', None)

        if files:
            try:
                ml_task = Dataset.objects.get(_id=bson.ObjectId(dataset_id)).ml_task
            except ObjectDoesNotExist:
                return ResponseError404NotFound(0, f'not found dataset: dataset_id={dataset_id}')
            if bundle_id == '' and len(files) > 1:
                return ResponseError400BadRequest(0, f'only one cover image must be uploaded.')

            fs = FileSystemStorage()
            results = []

            if not bundle_id or ml_task:
            # is file a cover image or image ml task
                valid_extension = FileExtensionValidator(allowed_extensions=['bmp', 'gif', 'jpg', 'jpeg', 'png', 'tif', 'webp'])
            else:
            # text ml task
                valid_extension = FileExtensionValidator(allowed_extensions=['txt'])
            for item in files:
                try:
                    valid_extension(item)
                except ValidationError: 
                    return ResponseError400BadRequest(0, f'invalid file type: file={item}')

                file = fs.save(dataset_id+'/'+item.name, item)
                serializer = FileUploadSerializer(data={
                    'dataset_id': dataset_id,
                    'bundle_id': bundle_id,
                    'name': item.name,
                    'url': fs.url(file)
                })
                if not serializer.is_valid():
                    return ResponseError400BadRequest(0, f'invalid file: file={item}')

                result = serializer.save()
                results.append(result)

                if not bundle_id:
                    Dataset.objects.filter(_id=bson.ObjectId(dataset_id)).update(cover_image=result.url)
                else:
                    item.open()
                    description = item.read().decode()[:25].replace('\n', '') if bundle_id and not ml_task else 'failed'

                    annotation_data = {
                        'dataset_id': dataset_id,
                        'bundle_id': bundle_id,
                        'file_id': str(result._id),
                        'description': description
                    }
                    annotation = AnnotationCreateDtoSerializer(data=annotation_data)
                    if not annotation.is_valid():
                        return ResponseError400BadRequest(0, f'invalid parameter: body={annotation_data}')
                    annotation.save()

            # ResponseMultipleItemsCreated가 필요
            return ResponseItemCreated(
                FileSerializer(results[0]).data,
                location=urllib.parse.urljoin(
                    f'{request.build_absolute_uri()}/', f'{results[0]._id}'
                )
            )
        else:
            return ResponseError400BadRequest(0, f'invalid files: files={request.FILES}')
            

class FileDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = File.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(FileSerializer(item).data)