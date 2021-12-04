from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Стандартная пагинация
    """
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 60

