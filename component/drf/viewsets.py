from django.db import transaction
from rest_framework import viewsets, mixins

from applications.system.models import AuditLog
from component.drf.mixins import ApiGenericMixin


class GenericViewSet(ApiGenericMixin, viewsets.GenericViewSet):
    """按需改造DRF默认的GenericViewSet类"""

    pass


class CreateModelAndLogMixin(mixins.CreateModelMixin):
    """
    Create a model instance and log.
    """

    @transaction.atomic()
    def perform_create(self, serializer):
        # 补充基础Model--MaintainerFieldsMixin中的字段
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        instance = serializer.save()
        obj, detail = instance.get_summary_title().split("/")
        AuditLog.simple_create(username, AuditLog.ADD, obj, detail)


class UpdateModelAndLogMixin(mixins.UpdateModelMixin):
    """
    Update a model instance and log.
    """

    @transaction.atomic()
    def perform_update(self, serializer):
        # 补充基础Model--MaintainerFieldsMixin中的字段
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        instance = serializer.save(updated_by=username)
        obj, detail = instance.get_summary_title().split("/")
        AuditLog.simple_create(username, AuditLog.MODIFY, obj, detail)


class DestroyModelAndLogMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance and log.
    """

    @transaction.atomic()
    def perform_destroy(self, instance):
        obj, detail = instance.get_summary_title().split("/")
        username = getattr(self, "request").user.username
        AuditLog.simple_create(username, AuditLog.DELETE, obj, detail)
        instance.delete()


class ModelAndLogViewSet(
    mixins.ListModelMixin,
    CreateModelAndLogMixin,
    mixins.RetrieveModelMixin,
    UpdateModelAndLogMixin,
    DestroyModelAndLogMixin,
    GenericViewSet,
):
    pass
