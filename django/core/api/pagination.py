from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    # Uma paginação padrão que fornece paginação baseada em número de página.

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
