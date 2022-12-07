import bson
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from pages.models import Page
from workbooks.models import Workbook

from misc.response import *
from misc import query_string


class ProblemsExplain(APIView):
    filter_keys = query_string.QueryStringFilterKeys({
        'workbook_name': str,
        'page_num': str,
        'prob_num': str,
    })

    def get(self, request):
        # query string parameters
        try:
            filter_map = query_string.parse_filtering(request.query_params, self.filter_keys)
        except query_string.QSParsingFilterError:
            return ResponseError400BadRequest(0, f'filter parsing error: query_params={request.query_params}')

        #
        workbook_name = filter_map.get('workbook_name')
        page_num = filter_map.get('page_num')
        prob_num = filter_map.get('prob_num')
        if not(workbook_name) or not(page_num) or not(prob_num):
            return ResponseError400BadRequest(0, f'invalid parameter: query_params={request.query_params}')

        #
        try:
            workbook = Workbook.objects.get(name=workbook_name)
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found workbook: workbook_name={workbook_name}')

        #
        queryset = Page.objects.filter(workbook_id=workbook._id, page_num=page_num)
        if queryset.count() == 0:
            return ResponseError404NotFound(0, f'not found page: page_num={page_num}')

        #
        try:
            page = queryset.get(problems={'prob_num': prob_num})
        except ObjectDoesNotExist:
            return ResponseError404NotFound(0, f'not found problem: prob_num={prob_num}')

        #
        problems = list(
            filter(lambda problem: problem.get('prob_num') == prob_num, page.problems)
        )
        if not problems:
            return ResponseError400BadRequest(0, f'internal error: problems={page.problems}')

        #
        problem = problems[0]
        return ResponseItem({
            'solving_url': problem.get('solving_url', ''),
            'similar_url': problem.get('similar_url', ''),
        })
