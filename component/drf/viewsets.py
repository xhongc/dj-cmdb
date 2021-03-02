from rest_framework import viewsets

from component.drf.mixins import ApiGenericMixin


class GenericViewSet(ApiGenericMixin, viewsets.GenericViewSet):
    """按需改造DRF默认的GenericViewSet类"""

    pass
