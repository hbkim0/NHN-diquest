import datetime
import urllib.parse
import bson

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc.utils import SearchModel
from misc import query_string

from .serializers import PageSerializer, PageCreateDtoSerializer, PageUpdateDtoSerializer
from .models import Page
from workbooks.models import Workbook
from images.models import ImageFSStorage

import fastjsonschema
from .compiled_labeled_page import validate

import io
from PIL import Image


def _validate_labeled_page(page):
    try:
        validate(page)
    except fastjsonschema.JsonSchemaException:
        return 0
    return 1


class PageList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'workbook_id': str,
        'labeled': int,
    })
    sortable_keys = [f.attname for f in Page._meta.concrete_fields]

    def post(self, request):
        serializer = PageCreateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')
        
        workbook_id = serializer.validated_data.get('workbook_id')
        if not bson.ObjectId.is_valid(workbook_id):
            return ResponseError400BadRequest(0, f'invalid parameter: workbook_id={workbook_id}')
        
        try:
            applied = Workbook.objects.get(_id=bson.ObjectId(workbook_id)).applied
        except ObjectDoesNotExist:
            return ResponseError400BadRequest(0, f'invalid parameter: workbook_id={workbook_id}')

        if applied:
            return ResponseError400BadRequest(0, f'applied workbook: workbook_id={workbook_id}')

        no_pages = Page.objects.filter(workbook_id=workbook_id).count() + 1

        modified_count = Workbook.objects.filter(_id=bson.ObjectId(workbook_id)).update(no_pages=no_pages, valid=0)
        if modified_count < 1:
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        result = serializer.save()
        
        return ResponseItemCreated(
            PageSerializer(result).data,
            location=urllib.parse.urljoin(
                f'{request.build_absolute_uri()}/', f'{result._id}'
            )
        )

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Page.objects.all()

        if len(filter_map):
            queryset = queryset.filter(**filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            PageSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )


class PageDetail(APIView):
    def get(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')
        
        try:
            item = Page.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        return ResponseItem(PageSerializer(item).data)

    def patch(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        serializer = PageUpdateDtoSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        try:
            item = Page.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')
        
        workbook_id = item.workbook_id
        try:
            applied = Workbook.objects.get(_id=bson.ObjectId(workbook_id)).applied
        except ObjectDoesNotExist:
            return ResponseError400BadRequest(0, f'invalid parameter: workbook_id={workbook_id}')

        if applied:
            return ResponseError400BadRequest(0, f'applied workbook: workbook_id={workbook_id}')        

        update_dict = serializer.validated_data.copy()
        update_dict.update(
            {
                'mod_date': datetime.datetime.utcnow(),
                'mod_id': 'user_id',
            }
        )
        
        storage = ImageFSStorage()

        sample_url = update_dict.get('sample_url')
        if sample_url != None:
            try:
                storage.open_image(sample_url)
            except FileNotFoundError:
                return ResponseError400BadRequest(0, f'invalid parameter: sample_url={sample_url}')

        original_url = update_dict.get('original_url')
        if original_url != None:
            try:
                file = storage.open_image(original_url).read()
            except FileNotFoundError:
                return ResponseError400BadRequest(0, f'invalid parameter: original_url={original_url}')
            image = Image.open(io.BytesIO(file))
            update_dict['width'], update_dict['height'] = image.size            
            update_dict['vector'] = list(range(512))

        new_item = PageSerializer(item).data.copy()
        new_item.update(update_dict)

        labeled_before = item.labeled
        labeled_after = _validate_labeled_page(new_item)

        update_dict['labeled'] = labeled_after
        new_item['labeled'] = labeled_after

        modified_count = Page.objects.filter(_id=bson.ObjectId(id)).update(**update_dict)
        if modified_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        if labeled_before != labeled_after:  # labeled status changed
            workbook_id = item.workbook_id
            if labeled_after == 1:
                unlabeled_count = Page.objects.filter(workbook_id=workbook_id, labeled=0).count()
                valid = 0 if unlabeled_count else 1
            else:
                valid = 0
            Workbook.objects.filter(_id=bson.ObjectId(workbook_id)).update(valid=valid)

        return ResponseItem(new_item)

    def delete(self, request, id):
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: id={id}')

        try:
            item = Page.objects.get(_id=bson.ObjectId(id))
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        workbook_id = item.workbook_id
        labeled = item.labeled

        try:
            applied = Workbook.objects.get(_id=bson.ObjectId(workbook_id)).applied
        except ObjectDoesNotExist:
            return ResponseError400BadRequest(0, f'invalid parameter: workbook_id={workbook_id}')

        if applied:
            return ResponseError400BadRequest(0, f'applied workbook: workbook_id={workbook_id}')

        deleted_count, _ = Page.objects.filter(_id=bson.ObjectId(id)).delete()

        if deleted_count < 1:
            return ResponseError404NotFound(0, f'not found: {id}')

        no_pages = Page.objects.filter(workbook_id=workbook_id).count()
        update_dict = {'no_pages': no_pages}
        if no_pages == 0:
            update_dict.update({'valid': 0})
        elif not labeled:
            if Page.objects.filter(workbook_id=workbook_id, labeled=0).count():
                update_dict.update({'valid': 0})
            else:
                update_dict.update({'valid': 1})
        Workbook.objects.filter(_id=bson.ObjectId(workbook_id)).update(**update_dict)

        return ResponseItemDeleted()


class PageCount(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'workbook_id': str,
        'labeled': int,
    })

    def get(self, request):
        try:
            filter_map = query_string.parse_filtering(request.query_params, self.filter_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        
        queryset = Page.objects.filter(**filter_map)

        return ResponseCount(
            count=queryset.count(), 
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]), 
        )


class Reindex(APIView):
    def post(self, request):
        storage = ImageFSStorage()
        pages = Page.objects.filter(labeled=1)
        model = SearchModel()

        input_dict = dict()
        for page in pages:
            page_id = page._id
            try:
                fin = storage.open_image(page.original_url)
            except FileNotFoundError as excp:
                continue
            input_dict[page_id] = fin.read()

        output_dict = model(input_dict)

        updated_cnt = 0
        for id in output_dict:
            new_vector = output_dict[id]
            modified_count = Page.objects.filter(_id=bson.ObjectId(id)).update(vector=new_vector)
            updated_cnt += modified_count

        return ResponseOK({'updated_cnt': updated_cnt})
