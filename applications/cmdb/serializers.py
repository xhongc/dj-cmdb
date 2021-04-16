from rest_framework import serializers

from applications.cmdb.models import CISchema, CIField, CI, Relation, CISchemaGroup, SchemaThroughRelation
from applications.subscription.signals import ci_create_signal
from applications.system.models import AuditLog


class CIFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIField
        fields = "__all__"


class ListCIFieldSerializer(serializers.ModelSerializer):
    # value_type = serializers.CharField(source="get_value_type_display")

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


class CISchemaWithNameAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CISchema
        fields = ("id", "name", "alias")


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
    field = ListCIFieldSerializer(many=True, read_only=True)

    class Meta:
        model = CISchema
        fields = ("id", "name", "alias", "is_show", "field", "icon_url")


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

    def validate(self, attrs):
        if SchemaThroughRelation.objects.filter(parent_id=attrs["source_id"], child_id=attrs["target_id"]).exists():
            raise serializers.ValidationError("关系已存在")
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CISerializer(serializers.Serializer):
    schema_id = serializers.IntegerField(required=True)
    field_value = serializers.JSONField(required=True, write_only=True)

    def validate(self, attrs):
        schema = CISchema.objects.get(id=attrs["schema_id"])
        # 验证传入的字段是否都是该模型的
        args_fields = set(attrs["field_value"].keys())
        all_fields = set(schema.field.values_list("name", flat=True))
        extra_fields = args_fields - all_fields
        if extra_fields == {"ci_id"}:
            self.instance = True
            return attrs
        elif extra_fields:
            raise serializers.ValidationError(f"{extra_fields}字段不属于该模型")
        return attrs

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            instance_id = validated_data["field_value"].pop("ci_id")
            self.instance = self.update(instance_id, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
            self._data = {"message": "修改成功"}
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def create(self, validated_data):
        try:
            instance = CI.objects.add(validated_data["schema_id"], validated_data["field_value"])
        except Exception as e:
            raise serializers.ValidationError(f'参数错误{str(e)}')
        else:
            ci_create_signal.send_robust(self.__class__, **validated_data)
            username = self.context.get("request").user.username
            AuditLog.simple_create(username, AuditLog.ADD, instance.schema.alias, instance.id)
            return instance

    def update(self, instance, validated_data):
        try:
            instance = CI.objects.modify(instance_id=instance, schema_id=validated_data["schema_id"],
                                         ci_data=validated_data["field_value"])
        except Exception as e:
            raise serializers.ValidationError(f'参数错误{str(e)}')
        else:
            ci_create_signal.send_robust(self.__class__, **validated_data)
            username = self.context.get("request").user.username
            AuditLog.simple_create(username, AuditLog.MODIFY, instance.schema.alias, instance.id)
            return instance


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
        try:
            return CI.objects.modify(validated_data["id"], validated_data["schema_id"], validated_data["field_value"])
        except Exception as e:
            raise serializers.ValidationError(f'参数错误{str(e)}')

    def update(self, instance, validated_data):
        pass
