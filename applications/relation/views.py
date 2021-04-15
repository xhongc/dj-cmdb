from rest_framework import mixins
from rest_framework.response import Response

from applications.cmdb.models import Relation, CISchema, SchemaThroughRelation
from applications.relation.serializers import RelationSerializer, TopoSchemaSerializer, TopoRelationSerializer
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


class TopoViewSets(GenericViewSet):
    serializer_class = RelationSerializer

    def list(self, request, *args, **kwargs):
        schema = CISchema.objects.all()
        relation = SchemaThroughRelation.objects.all()

        nodes_serializer = TopoSchemaSerializer(schema, many=True).data
        relation_serializer = TopoRelationSerializer(relation, many=True).data
        data = {
            "nodes": nodes_serializer,
            "edges": relation_serializer
        }
        return Response(data)
