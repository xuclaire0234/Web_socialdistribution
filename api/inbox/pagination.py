# 2023-03-04
# inbox/pagination.py

from collections import OrderedDict
from rest_framework.response import Response

from author.models import Author
from utils.node_comm import NodeComm
from utils.pagination import CustomPagination

NodeComm = NodeComm()

import logging
logger = logging.getLogger('django')
rev = 'rev: $xFgLu67$x'

class InboxPagination(CustomPagination):
    lookup_url_kwarg = 'author_uuid'

    def get_paginated_response(self, inbox_items):
        author_uuid = self.request.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        author_node_id = author_obj.get_node_id()

        lookup_inbox_items = NodeComm.get_objects(inbox_items)

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('type', 'inbox'),
            ('author', author_node_id),
            ('items', lookup_inbox_items)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                    'count': {
                        'type': 'integer',
                        'example': 10
                    },
                    'type': {
                        'type': 'string',
                        'example': 'inbox'
                    },
                    'author': {
                        'type': 'string',
                        'format': 'uri',
                        'example': 'http://api.example.com/api/authors/12345678-90ab-cdef-ghij-klmnopqrstuv'
                    },
                    'items': schema,
              },
          }
