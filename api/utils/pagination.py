# 2023-02-21
# utils/pagination.py

from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('items', data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                    'count': {
                        'type': 'integer',
                        'example': 10
                    },
                    'items': schema,
              },
          }
