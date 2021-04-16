from rest_framework import mixins

from applications.system.filters import AuditLogFilter
from applications.system.models import AuditLog
from applications.system.serializers import AuditLogSerializer
from component.drf.pagination import CustomPageNumberPagination
from component.drf.viewsets import GenericViewSet


class AuditLogViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    list: 操作日志
    """

    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    filterset_class = AuditLogFilter
    pagination_class = CustomPageNumberPagination
