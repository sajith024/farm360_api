from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "pagination": {
                    "page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "count": self.page.paginator.count,
                },
            }
        )
