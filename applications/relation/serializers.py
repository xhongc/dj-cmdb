from rest_framework import serializers

from applications.cmdb.models import Relation, CISchema, SchemaThroughRelation


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = "__all__"


class TopoSchemaSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    label = serializers.CharField(source="alias")
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.icon_url.replace("cmdb-", "")

    class Meta:
        model = CISchema
        fields = ("id", "label", "text")


class TopoRelationSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="parent_id")
    target = serializers.CharField(source="child_id")
    label = serializers.CharField(source="relation.alias")

    class Meta:
        model = SchemaThroughRelation
        fields = ("source", "target", "label")
