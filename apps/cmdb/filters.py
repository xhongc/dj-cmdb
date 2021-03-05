import django_filters as filters
from django.db.models import Q


class CIFilter(filters.FilterSet):
    meta = filters.CharFilter(method="filter_meta")
    schema_id = filters.NumberFilter()

    @staticmethod
    def filter_meta(queryset, key, value):
        if value in [1, '1', 'True', 'true']:
            return queryset.filter(Q(meta__is_required=True) | Q(meta__is_unique=True))
        else:
            return queryset.filter(Q(meta__is_required=False) | Q(meta__is_unique=False))
