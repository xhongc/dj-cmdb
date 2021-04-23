import math
from collections import defaultdict

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.cmdb.filters import CIFilter
from applications.cmdb.models import CISchema, CIField, CI, MODEL_TYPE_MAP, SchemaThroughRelation, CISchemaGroup, \
    Relation, CIThroughRelation
from applications.cmdb.serializers import CISchemaSerializer, CIFieldSerializer, CISerializer, CIUpdateSerializer, \
    CISchemaRelationSerializer, CISchemaGroupSerializer, CreateCISchemaGroupSerializer, ListCIFieldSerializer, \
    ReadCISchemaSerializer, CISchemaWithNameAliasSerializer, CIRelationSerializer, SchemaRelationSelectSerializer, \
    CIThroughRelationSerializer
from applications.relation.serializers import RelationSerializer
from applications.system.models import AuditLog
from component.drf.viewsets import GenericViewSet, ModelAndLogViewSet


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
    filterset_fields = {"name": ("exact",), "id": ("exact",), "is_show": ("exact",)}

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
        t = SchemaThroughRelation.objects.create(parent_id=serializer.validated_data['source_id'],
                                                 child_id=serializer.validated_data['target_id'],
                                                 relation_id=serializer.validated_data['relation_id'])
        AuditLog.simple_create(request.user.username, AuditLog.ADD, "关联关系:",
                               f"{t.parent.alias}={t.relation.alias}>{t.child.alias}")
        return Response({})

    @action(methods=["get"], detail=False)
    def get_relation_select(self, request, *args, **kwargs):
        q = self.get_queryset()
        r = Relation.objects.all()
        schema_serializer = CISchemaWithNameAliasSerializer(q, many=True).data
        relation_serializer = RelationSerializer(r, many=True).data
        return Response({"schema": schema_serializer, "relation": relation_serializer})


class CISchemaGroupViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin, GenericViewSet):
    queryset = CISchemaGroup.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCISchemaGroupSerializer
        return CISchemaGroupSerializer


class CIFieldViewSet(ModelAndLogViewSet):
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
    queryset = CI.objects.all().order_by('-id')
    lookup_field = "schema_id"

    def get_serializer_class(self):
        if self.action == "update":
            return CIUpdateSerializer
        elif self.action == "add_relation":
            return CIRelationSerializer
        return CISerializer

    def retrieve(self, request, *args, **kwargs):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        offset = (page - 1) * page_size
        # 模型条目ids
        ci_ids = self.get_queryset().filter(**kwargs).values_list('id', flat=True)[offset:page_size * page]
        ci_count = self.get_queryset().filter(**kwargs).count()
        # union所有值model
        none_queryset = CI.objects.none()
        queryset = []
        for value_model in MODEL_TYPE_MAP.values():
            queryset.append(
                value_model.objects.filter(ci_id__in=list(ci_ids)).values_list("ci_id", "field__name", "value"))
        union_query = none_queryset.union(*queryset).order_by('-ci_id')
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

    @action(methods=["post"], detail=False)
    def add_relation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CIThroughRelation.objects.create(schema_relation_id=serializer.validated_data["schema_relation_id"],
                                         parent_id=serializer.validated_data["source_id"],
                                         child_id=serializer.validated_data["target_id"])
        return Response({})

    @action(methods=["get"], detail=True)
    def get_relation_select(self, request, *args, **kwargs):
        schema_relation = SchemaThroughRelation.objects.filter(parent_id=kwargs["schema_id"])
        schema_relation_serializer = SchemaRelationSelectSerializer(schema_relation, many=True).data
        return Response(schema_relation_serializer)


class CIThroughRelationViewSets(mixins.ListModelMixin, GenericViewSet):
    queryset = CIThroughRelation.objects.all()
    serializer_class = CIThroughRelationSerializer
    filterset_fields = {"parent_id": ("exact",)}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True).data
        relation_data = defaultdict(lambda: defaultdict(list))
        for relation in serializer:
            relation_data[relation["schema_relation"]["id"]]["child_ids"].append(relation["child"])
            relation_data[relation["schema_relation"]["id"]]["relation_name"] =\
                f"{relation['schema_relation']['relation']}-{relation['schema_relation']['child_alias']}"
        return Response(relation_data)
