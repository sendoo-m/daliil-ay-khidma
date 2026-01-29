"""
API Pagination
==============
Custom pagination classes
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination:
    - 20 results per page by default
    - Client can control page size up to 100
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Large results pagination:
    - 50 results per page by default
    - Client can control page size up to 200
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
