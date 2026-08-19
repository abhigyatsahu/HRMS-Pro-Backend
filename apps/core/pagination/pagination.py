from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings

class StandardPagination(PageNumberPagination):
    """
    Standard pagination for HRMS.
    """
    page_size = settings.HRMS_PAGINATION[
        "DEFAULT_PAGE_SIZE"
    ]
    page_size_query_param = "page_size"
    max_page_size = settings.HRMS_PAGINATION[
        "MAX_PAGE_SIZE"
    ]
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(

            {

                "success": True,

                "message": "Data fetched successfully.",

                "data": {

                    "items": data,

                    "pagination": {

                        "page": self.page.number,

                        "page_size": self.get_page_size(
                            self.request
                        ),

                        "total_items": self.page.paginator.count,

                        "total_pages": self.page.paginator.num_pages,

                        "has_next": self.page.has_next(),

                        "has_previous": self.page.has_previous(),

                    }

                }

            }

        )