import django_filters
from sell.models import *

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Products
        fields = ['price', 'release_date']