import io
import sys
import bson
import datetime
import pathlib

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from misc.response import *
from misc.utils import RecognitionModel, SearchModel, get_resized_shape
from misc import query_string

from .models import Log
from .serializers import DnRRequestSerializer, ScoreRequestSerializer, LogSerializer

from images.models import ImageFSStorage
from workbooks.models import Workbook
from workbooks.serializers import WorkbookSerializer
from pages.models import Page
from pages.serializers import PageSerializer

import numpy as np
import cv2
import imutils
from scipy import spatial
from imutils.perspective import four_point_transform


def _detect(image):
    h, w, _ = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    area = gray.shape[0] * gray.shape[1]

    max_cnt_area = 0
    max_cnt = []
    for t in range(100, 255, 50):
        edged = cv2.adaptiveThreshold(gray, t, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        edged = cv2.GaussianBlur(edged, (5, 5), 0)
        edged = cv2.edgePreservingFilter(edged, flags=1, sigma_s=45, sigma_r=0.2)
        edged = cv2.Canny(edged, 0, 0)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        findCnt = None
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                findCnt = approx
                break

        if findCnt is None:
            continue
        cnt_area = cv2.contourArea(findCnt)
        if cnt_area < area * 0.5:
            continue
        if cnt_area > max_cnt_area:
            max_cnt_area = cnt_area
            max_cnt = findCnt
            if cnt_area > area * 0.75:
                break
    
    if not len(max_cnt):
        return None

    findCnt = max_cnt
    contour_image = image.copy()
    cv2.drawContours(contour_image, [findCnt], -1, (0, 255, 0), 2)
    
    output = image.copy()
    transform_image = four_point_transform(output, findCnt.reshape(4, 2))
    transform_image = cv2.resize(transform_image, [w, h])

    return transform_image


def _search(image, threshold=0.5):
    model = SearchModel()
    image_vector = model(image)

    id_list = [workbook._id for workbook in Workbook.objects.filter(applied=1)]
    pages = Page.objects.filter(workbook_id__in=id_list) 
    min_dist = 1
    for page in pages:
        page_vector = page.vector
        dist = spatial.distance.cosine(image_vector, page_vector)
        if dist < min_dist:
            min_dist = dist
            searched = page

    if min_dist > threshold:
        return {'success': 0}
    return {'success': 1, 'page': searched}


def _recognize(image, page):
    problems = page.problems
    w, h = page.width, page.height
    image = cv2.resize(image, [w, h])
    boxed_image = image.copy()
    model = RecognitionModel()

    predictions = list()
    for problem in problems:
        answers = list()
        cropped = list()
        labels = problem.get('labels')
        for label in labels:
            bbox = label.get('bbox')
            cv2.rectangle(boxed_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 5)
            cropped.append(image[bbox[1]:bbox[3], bbox[0]:bbox[2]])

        answers = model(cropped)
        predictions.append(
            {
                'prob_num': problem.get('prob_num'),
                'answers': answers
            }
        )

    results = {
        'boxed_image': boxed_image,
        'predictions': predictions
    }

    return results


class InferDnR(APIView):
    def post(self, request):
        request_serializer = DnRRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        input_url = request_serializer.validated_data.get('input_url')
        user_id = request_serializer.validated_data.get('user_id')

        storage = ImageFSStorage()
        try:
            fin = storage.open_image(input_url)
        except FileNotFoundError:
            return ResponseError400BadRequest(0, f'invalid parameter: input_url={input_url}')
        image = cv2.imdecode(np.fromstring(fin.read(), dtype=np.uint8), cv2.IMREAD_COLOR)
        
        h, w, _ = image.shape
        w, h = get_resized_shape(w, h, 1000)
        image = cv2.resize(image, [w, h])

        detected_image = _detect(image)
        if isinstance(detected_image, np.ndarray):
            search_results = _search(detected_image)  # {success, page}
            success = search_results.get('success')
        else:
            success = 0

        results = {'success': success, 'input_url': input_url, 'user_id': user_id}
        if success:
            page = search_results.get('page')
            recognize_results = _recognize(detected_image, page)  # {boxed image, predictions}
            
            # boxed image
            boxed_image = recognize_results.get('boxed_image')
            _, encoded_image = cv2.imencode('.jpg', boxed_image)
            image_io = io.BytesIO(encoded_image)
            f = InMemoryUploadedFile(image_io, 'ImageField', f'boxed_{pathlib.Path(fin.filename).with_suffix(".jpg")}', 'image/jpeg', sys.getsizeof(image_io), None)
            boxed_urls = storage.save_images([f])
            results['boxed_url'] = boxed_urls[0]

            # page and workbook
            workbook = Workbook.objects.get(_id=bson.ObjectId(page.workbook_id))
            results['workbook'] = WorkbookSerializer(workbook).data
            results['page'] = PageSerializer(page).data

            results['predictions'] = recognize_results.get('predictions')

        if request_serializer.validated_data.get('log'):
            log_data = results.copy()
            if success:
                log_data['scoring'] = log_data.pop('predictions')
            log_data['reg_date'] = datetime.datetime.utcnow()
            log_data['reg_id'] = 'user_id'

            log_object = Log.objects.create(**log_data)
            results['log_id'] = str(log_object._id)

        return ResponseOK(results)


class InferScore(APIView):
    def post(self, request):
        request_serializer = ScoreRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        id = request_serializer.validated_data.get('page_id')
        if not bson.ObjectId.is_valid(id):
            return ResponseError400BadRequest(0, f'invalid parameter: page_id={id}')
        try:
            page = Page.objects.get(_id=bson.ObjectId(id), labeled=1)
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found: {id}')

        predictions = request_serializer.validated_data.get('predictions')
        if len(page.problems) != len(predictions):
            return ResponseError400BadRequest(0, f'invalid parameter: body={request.data}')

        log_id = request_serializer.validated_data.get('log_id')
        if log_id:
            if not bson.ObjectId.is_valid(log_id):
                return ResponseError400BadRequest(0, f'invalid parameter: log_id={log_id}')
            try:
                scoring = Log.objects.get(_id=bson.ObjectId(log_id)).scoring
            except ObjectDoesNotExist:
                return ResponseError400BadRequest(0, f'invalid parameter: log_id={log_id}')

        results = list()
        prob_num_err = False
        for idx, prediction in enumerate(predictions):
            prob_num = prediction.get('prob_num')
            custom_answers = prediction.get('answers')
            if prob_num != page.problems[idx].get('prob_num'):
                prob_num_err = True
                break

            labels = list()
            for label in page.problems[idx].get('labels'):
                labels.append(label.get('label'))

            correct = 1 if custom_answers == labels else 0

            results.append({
                'prob_num': prob_num,
                'solving_url': page.problems[idx].get('solving_url'),
                'similar_url': page.problems[idx].get('similar_url'),
                'correct': correct
            })
            
            if log_id:
                scoring[idx].update({
                    'labels': labels, 
                    'custom_answers': custom_answers, 
                    'correct': correct
                })

        if prob_num_err:
            return ResponseError400BadRequest(0, f'invalid parameter: predictions={predictions}')

        if log_id:
            Log.objects.filter(_id=bson.ObjectId(log_id)).update(scoring=scoring)

        return ResponseOK(results)


class LogList(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'success': int,
        'workbook_id': str,
        'page_id': str,
        'user_id': str,
    })
    sortable_keys = [f.attname for f in Log._meta.concrete_fields]

    def get(self, request):
        try:
            filter_map, offset, limit, sort_by = query_string.parse(request.query_params, self.filter_keys, self.sortable_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')
        except query_string.QSParsingPaginationError:
            return ResponseError400BadRequest(0, f'pagination parsing error: query_params={request.query_params}')
        except query_string.QSParsingSortingError:
            return ResponseError400BadRequest(0, f'sorting parsing error: query_params={request.query_params}')

        queryset = Log.objects.all()

        if len(filter_map):
            new_filter_map = filter_map.copy()
            if new_filter_map.get('workbook_id'):
                workbook_id = new_filter_map.pop('workbook_id')
                queryset = queryset.filter(workbook={'_id': workbook_id})
            if new_filter_map.get('page_id'):
                page_id = new_filter_map.pop('page_id')
                queryset = queryset.filter(page={'_id': page_id})
            queryset = queryset.filter(**new_filter_map)
        if len(sort_by):
            queryset = queryset.order_by(*sort_by)

        return ResponseList(
            queryset.count(),
            LogSerializer(queryset[offset:(offset+limit)], many=True).data,
            limit=limit,
            offset=offset,
            sort_by=','.join(sort_by),
            filtering='&'.join([f'{k}={v}' for k, v in filter_map.items()]),
        )
