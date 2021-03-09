from rest_framework import mixins

from apps.cmdb.models import Relation
from apps.relation.serializers import RelationSerializer
from component.drf.viewsets import GenericViewSet


class RelationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    list:查看字段
    create:创建字段
    """
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
