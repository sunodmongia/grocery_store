from rest_framework.pagination import PageNumberPagination

class TenPerPage(PageNumberPagination):
    page_size = 10