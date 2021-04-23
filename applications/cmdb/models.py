import json
from datetime import datetime

from django.db import models, transaction
from django.db.models import Q

from applications.cmdb.constants import VALUE_TYPE_MAP, ValueTypeEnum


class CISchema(models.Model):
    name = models.CharField("模型名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("模型别名", max_length=32, null=False, blank=False)
    desc = models.CharField("描述", max_length=255, default='', null=True, blank=True)
    icon_url = models.CharField("图标", max_length=255, default='', null=True, blank=True)

    relation = models.ManyToManyField("self", related_name="relation_schema", through="SchemaThroughRelation",
                                      symmetrical=False, through_fields=('parent', 'child'))
    group = models.ForeignKey("CISchemaGroup", related_name="schema", on_delete=models.CASCADE, db_constraint=False,
                              null=True)
    is_show = models.BooleanField("是否展示", default=False)

    class Meta:
        verbose_name = "模型"


class CISchemaGroup(models.Model):
    name = models.CharField("模型分组名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("模型分组别名", max_length=32, default='')

    class Meta:
        verbose_name = "模型分组"


class CIFieldManager(models.Manager):
    def get_field_mapping(self, names: list, schema_id):
        display_values = ("id", "name", "value_type", "meta", "alias")
        qs = self.filter(Q(name__in=names) | Q(meta__is_required=True, schema_id=schema_id)).values(*display_values)
        return {q["name"]: q for q in qs}


class CIField(models.Model):
    name = models.CharField("字段名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("字段别名", max_length=32, default='')

    value_type = models.CharField("值的类型", choices=VALUE_TYPE_MAP, blank=False, null=False, max_length=2)
    meta = models.JSONField("字段属性", default=dict)
    schema = models.ForeignKey("CISchema", related_name="field", on_delete=models.CASCADE, db_constraint=False,
                               null=False, blank=False, default='')
    objects = CIFieldManager()

    class Meta:
        verbose_name = "模型字段"

    def get_summary_title(self):
        return f"{self.schema.alias}:属性:/{self.alias}"


class Relation(models.Model):
    name = models.CharField("关系名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("字段别名", max_length=32, default='')


class SchemaThroughRelation(models.Model):
    parent = models.ForeignKey("CISchema", related_name="_child", on_delete=models.CASCADE, db_constraint=False)
    child = models.ForeignKey("CISchema", related_name="_parent", on_delete=models.CASCADE, db_constraint=False)
    relation = models.ForeignKey("Relation", related_name="ci_schema", on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = "模型和关系穿梭表"


class CIIntValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.IntegerField("整型值", null=False, blank=False)

    class Meta:
        verbose_name = "整型值"


class CIIndexIntValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.IntegerField("索引整型值", null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "索引整型值"


class CIFloatValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.FloatField("浮点型值", null=False, blank=False)

    class Meta:
        verbose_name = "浮点型值"


class CIIndexFloatValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.FloatField("索引浮点型值", null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "索引浮点型值"


class CITextValue(models.Model):
    ALLOW_INDEX = False

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.TextField("文本型值", null=False, blank=False)

    class Meta:
        verbose_name = "文本型值"


class CIDatetimeValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.DateTimeField("日期时间值", null=False, blank=False)

    class Meta:
        verbose_name = "日期时间值"


class CIIndexDatetimeValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.DateTimeField("索引日期时间值", null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "索引日期时间值"


class CIDateValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.DateField("日期值", null=False, blank=False)

    class Meta:
        verbose_name = "日期值"


class CIIndexDateValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.DateField("索引日期值", null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "索引日期值"


class CITimeValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.TimeField("时间值", null=False, blank=False)

    class Meta:
        verbose_name = "时间值"


class CIIndexTimeValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.TimeField("索引时间值", null=False, blank=False, db_index=True)

    class Meta:
        verbose_name = "索引时间值"


class CIJsonValue(models.Model):
    ALLOW_INDEX = False

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.JSONField("JSON值", null=False, blank=False)

    class Meta:
        verbose_name = "JSON值"


class CICharValue(models.Model):
    ALLOW_INDEX = True

    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.CharField("字符串值", null=False, blank=False, max_length=255)

    class Meta:
        verbose_name = "字符串值"


class CIIndexCharValue(models.Model):
    ci = models.ForeignKey("CI", on_delete=models.CASCADE, db_constraint=False)
    field = models.ForeignKey("CIField", on_delete=models.CASCADE, db_constraint=False)
    value = models.CharField("索引字符串值", null=False, blank=False, db_index=True, max_length=255)

    class Meta:
        verbose_name = "索引字符串值"


MODEL_TYPE_MAP = {
    ValueTypeEnum.INT: CIIntValue,
    ValueTypeEnum.FLOAT: CIFloatValue,
    ValueTypeEnum.TEXT: CITextValue,
    ValueTypeEnum.DATETIME: CIDatetimeValue,
    ValueTypeEnum.DATE: CIDateValue,
    ValueTypeEnum.TIME: CITimeValue,
    ValueTypeEnum.JSON: CIJsonValue,
    ValueTypeEnum.CHAR: CICharValue,
    ValueTypeEnum.ENUM: CICharValue,
}
VALUE_VALIDATE = {
    ValueTypeEnum.INT: int,
    ValueTypeEnum.FLOAT: float,
    ValueTypeEnum.TEXT: str,
    ValueTypeEnum.DATETIME: lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
    ValueTypeEnum.DATE: lambda x: datetime.strptime(x, "%Y-%m-%d"),
    ValueTypeEnum.TIME: lambda x: datetime.strptime(x, "%H:%M:%S"),
    ValueTypeEnum.JSON: json.loads,
    ValueTypeEnum.CHAR: str,
    ValueTypeEnum.ENUM: str,
}


class CIManager(models.Manager):
    @staticmethod
    def items_exists(schema_id, keys):
        return CIField.objects.filter(schema_id=schema_id, name__in=keys).count() == len(keys)

    def add(self, schema_id, ci_data: dict):
        """
        ci_data: {field:value...}
        """
        with transaction.atomic():
            # 验证是否字段都属于改模型
            if not self.items_exists(schema_id, list(ci_data.keys())):
                raise Exception("创建字段不属于/或不存在")
            ci = self.create(schema_id=schema_id)
            ci_id = ci.id
            field_mapping = CIField.objects.get_field_mapping(names=list(ci_data.keys()), schema_id=schema_id)
            # 验证必填字段
            if set(field_mapping.keys()) != set(ci_data.keys()):
                miss_field = set(field_mapping.keys()) - set(ci_data.keys())
                raise Exception(f"{miss_field}字段为必填")
            for field, value in ci_data.items():
                if not value:
                    continue
                value_model, validated_value = self.verify_fields(field_mapping, field, value)
                value_model.objects.create(ci_id=ci_id, field_id=field_mapping[field]["id"], value=validated_value)
        return ci

    def verify_fields(self, field_mapping, field, value):
        """必須验证必填"""
        value_model = MODEL_TYPE_MAP[field_mapping[field]["value_type"]]
        value_validate = VALUE_VALIDATE[field_mapping[field]["value_type"]]
        # 验证值是否是预设类型
        try:
            validated_value = value_validate(value)
        except Exception as e:
            field_alias = field_mapping[field]['alias']
            raise Exception(f"<{field_alias}>:{value} 类型不符合：{e}")
        meta_data = field_mapping[field]["meta"]
        if meta_data.get("is_unique", False):
            if hasattr(self, "instance_id"):
                ci_id = self.instance_id
                value_filter = value_model.objects.filter(field_id=field_mapping[field]["id"], value=value).exclude(
                    ci_id=ci_id)
            else:
                value_filter = value_model.objects.filter(field_id=field_mapping[field]["id"], value=value)
            if value_filter.exists():
                field_alias = field_mapping[field]['alias']
                raise Exception(f"<{field_alias}>:{value} 已存在")
        return value_model, validated_value

    def modify(self, instance_id, schema_id, ci_data: dict):
        with transaction.atomic():
            if not self.items_exists(schema_id, list(ci_data.keys())):
                raise Exception("创建字段不属于/或不存在")
            ci_id = instance_id
            self.instance_id = ci_id
            field_mapping = CIField.objects.get_field_mapping(names=list(ci_data.keys()), schema_id=schema_id)
            for field, value in ci_data.items():
                value_model, validated_value = self.verify_fields(field_mapping, field, value)
                value_model.objects.update_or_create(ci_id=ci_id, field_id=field_mapping[field]["id"],
                                                     defaults={"value": validated_value})
        return CI.objects.get(id=ci_id)


class CI(models.Model):
    schema = models.ForeignKey("CISchema", on_delete=models.CASCADE, related_name="item", db_constraint=False)
    objects = CIManager()

    class Meta:
        verbose_name = "配置项"


class CIThroughRelation(models.Model):
    schema_relation = models.ForeignKey("SchemaThroughRelation", related_name="inst_relation", on_delete=models.CASCADE,
                                        db_constraint=False)
    parent = models.ForeignKey("CI", related_name="_child", on_delete=models.CASCADE, db_constraint=False)
    child = models.ForeignKey("CI", related_name="_parent", on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = "实例和模型关系穿梭表"
