from rest_framework import serializers

from applications.cmdb.models import CISchema, CIField, CI, Relation, CISchemaGroup, SchemaThroughRelation


class CIFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIField
        fields = "__all__"


class ListCIFieldSerializer(serializers.ModelSerializer):
    value_type = serializers.CharField(source="get_value_type_display")

    class Meta:
        model = CIField
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(ListCIFieldSerializer, self).to_representation(instance)
        ret["is_required"] = str(ret["meta"].get("is_required", False))
        ret["is_unique"] = str(ret["meta"].get("is_unique", False))
        return ret


class CISchemaSerializer(serializers.ModelSerializer):
    field = CIFieldSerializer(many=True, read_only=True)

    class Meta:
        model = CISchema
        fields = "__all__"


class SchemaThroughRelationSerializer(serializers.ModelSerializer):
    relation = serializers.CharField(source="relation.alias")
    source = serializers.CharField(source="parent.alias")
    target = serializers.CharField(source="child.alias")

    class Meta:
        model = SchemaThroughRelation
        fields = "__all__"


class ReadCISchemaSerializer(serializers.ModelSerializer):
    field = ListCIFieldSerializer(many=True, read_only=True)

    relation = SchemaThroughRelationSerializer(many=True, source="_child")
    relation_schema = SchemaThroughRelationSerializer(many=True, source="_parent")

    class Meta:
        model = CISchema
        fields = "__all__"


class SimpleCISchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CISchema
        fields = ("id", "name", "alias")


class CISchemaGroupSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    schema = SimpleCISchemaSerializer(many=True)

    class Meta:
        model = CISchemaGroup
        fields = "__all__"


class CreateCISchemaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CISchemaGroup
        fields = "__all__"


class CISchemaRelationSerializer(serializers.Serializer):
    source_id = serializers.IntegerField(required=True)
    target_id = serializers.IntegerField(required=True)
    relation_id = serializers.IntegerField(required=True)

    def validate_source_id(self, source_id):
        if not CISchema.objects.filter(id=source_id).exists():
            raise serializers.ValidationError('源模型不存在')
        return source_id

    def validate_target_id(self, target_id):
        if not CISchema.objects.filter(id=target_id).exists():
            raise serializers.ValidationError('目标模型不存在')
        return target_id

    def validate_relation_id(self, relation_id):
        if not Relation.objects.filter(id=relation_id).exists():
            raise serializers.ValidationError('关系不存在')
        return relation_id

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CISerializer(serializers.Serializer):
    schema_id = serializers.IntegerField(required=True)
    field_value = serializers.JSONField(required=True, write_only=True)

    def validate(self, attrs):
        schema = CISchema.objects.get(id=attrs["schema_id"])
        args_fields = set(attrs["field_value"].keys())
        all_fields = set(schema.field.values_list("name", flat=True))
        extra_fields = args_fields - all_fields
        if extra_fields:
            raise serializers.ValidationError(f"{extra_fields}字段不属于该模型")
        return attrs

    def create(self, validated_data):
        try:
            return CI.objects.add(validated_data["schema_id"], validated_data["field_value"])
        except Exception as e:
            raise serializers.ValidationError(f'参数错误{str(e)}')

    def update(self, instance, validated_data):
        pass


class CIUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    field_value = serializers.JSONField(required=True)

    def validate(self, attrs):
        try:
            ci = CI.objects.get(id=attrs["id"])
        except CI.DoesNotExist as e:
            raise serializers.ValidationError(f"id不存在：{str(e)}")
        else:
            args_fields = set(attrs["field_value"].keys())
            all_fields = set(ci.schema.field.values_list("name", flat=True))
            extra_fields = args_fields - all_fields
            if extra_fields:
                raise serializers.ValidationError(f"{extra_fields}字段不属于该模型")
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
