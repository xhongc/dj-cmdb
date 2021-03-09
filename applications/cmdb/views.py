import math
from collections import defaultdict

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.cmdb.filters import CIFilter
from apps.cmdb.models import CISchema, CIField, CI, MODEL_TYPE_MAP, SchemaThroughRelation, CISchemaGroup
from apps.cmdb.serializers import CISchemaSerializer, CIFieldSerializer, CISerializer, CIUpdateSerializer, \
    CISchemaRelationSerializer, CISchemaGroupSerializer, CreateCISchemaGroupSerializer, ListCIFieldSerializer, \
    ReadCISchemaSerializer
from component.drf.viewsets import GenericViewSet


class CISchemaViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    list:查看模型
    create:新增模型
    """
    queryset = CISchema.objects.all()
    filterset_fields = {"name": ("exact",), "id": ("exact",)}

    def get_serializer_class(self):
        if self.action == "add_relation":
            return CISchemaRelationSerializer
        elif self.action == "create":
            return CISchemaSerializer
        elif self.action == "retrieve":
            return ReadCISchemaSerializer
        return CISchemaSerializer

    @action(methods=["post"], detail=False)
    def add_relation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SchemaThroughRelation.objects.create(parent_id=serializer.validated_data['source_id'],
                                             child_id=serializer.validated_data['target_id'],
                                             relation_id=serializer.validated_data['relation_id'])
        return Response({})


class CISchemaGroupViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin, GenericViewSet):
    queryset = CISchemaGroup.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCISchemaGroupSerializer
        return CISchemaGroupSerializer


class CIFieldViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    """
    list:查看字段
    create:创建字段
    """
    queryset = CIField.objects.all()
    filter_class = CIFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ListCIFieldSerializer
        return CIFieldSerializer


class CIViewSet(mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                GenericViewSet):
    """
    retrieve:根据模型id查每条配置项数据
    create:新增配置项
    """
    queryset = CI.objects.all()
    lookup_field = "schema_id"

    def get_serializer_class(self):
        if self.action == "update":
            return CIUpdateSerializer
        return CISerializer

    def retrieve(self, request, *args, **kwargs):
        page = request.data.get("page", 1)
        page_size = request.data.get("page_size", 10)
        offset = (page - 1) * page_size
        # 模型条目ids
        ci_ids = self.get_queryset().filter(**kwargs).values_list('id', flat=True)[offset:page_size]
        ci_count = self.get_queryset().filter(**kwargs).count()
        # union所有值model
        none_queryset = CI.objects.none()
        queryset = []
        for value_model in MODEL_TYPE_MAP.values():
            queryset.append(
                value_model.objects.filter(ci_id__in=list(ci_ids)).values_list("ci_id", "field__name", "value"))
        union_query = none_queryset.union(*queryset)
        # 根据ci—id聚合字段-值
        ci_dict = defaultdict(dict)
        for ci_id, field_name, value in union_query:
            ci_dict[ci_id][field_name] = value
            ci_dict[ci_id]["ci_id"] = ci_id

        return Response({
            "page": page,
            "total_page": math.ceil(ci_count / page_size),
            "count": ci_count,
            "item": list(ci_dict.values())
        })

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ci = self.get_queryset().filter(id=serializer.validated_data["id"], **kwargs).first()
        field_value = serializer.validated_data["field_value"]
        CI.objects.modify(instance_id=ci.id, schema_id=kwargs["schema_id"], ci_data=field_value)
        return Response({})
