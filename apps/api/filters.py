"""Mobile-friendly query filters for the public API."""

from django_filters import rest_framework as filters

from apps.deals.models import Deal
from apps.directory.models import Business
from apps.products.models import Product


class BusinessFilter(filters.FilterSet):
    governorate = filters.NumberFilter(field_name='district__city__governorate_id')
    city = filters.NumberFilter(field_name='district__city_id')
    min_rating = filters.NumberFilter(field_name='average_rating', lookup_expr='gte')

    class Meta:
        model = Business
        fields = [
            'business_type', 'category', 'district', 'governorate', 'city',
            'is_featured', 'min_rating',
        ]


class ProductFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='business__category_id')
    governorate = filters.NumberFilter(field_name='business__district__city__governorate_id')
    city = filters.NumberFilter(field_name='business__district__city_id')
    district = filters.NumberFilter(field_name='business__district_id')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = [
            'product_type', 'business', 'category', 'governorate', 'city',
            'district', 'is_featured', 'min_price', 'max_price',
        ]


class DealFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='business__category_id')
    governorate = filters.NumberFilter(field_name='business__district__city__governorate_id')
    city = filters.NumberFilter(field_name='business__district__city_id')
    district = filters.NumberFilter(field_name='business__district_id')

    class Meta:
        model = Deal
        fields = [
            'deal_type', 'business', 'category', 'governorate', 'city',
            'district', 'is_featured',
        ]
