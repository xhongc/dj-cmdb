from django.db import models, transaction

from apps.cmdb.constants import VALUE_TYPE_MAP, ValueTypeEnum


class CISchema(models.Model):
    name = models.CharField("模型名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("模型别名", max_length=32, null=False, blank=False)
    desc = models.CharField("描述", max_length=255, default='', null=True, blank=True)
    icon_url = models.CharField("图标", max_length=255, default='', null=True, blank=True)

    relation = models.ManyToManyField("self", related_name="relation_schema", through="SchemaThroughRelation",
                                      symmetrical=False, through_fields=('parent', 'child'))
    group = models.ForeignKey("CISchemaGroup", related_name="schema", on_delete=models.CASCADE, db_constraint=False,
                              null=True)

    class Meta:
        verbose_name = "模型"


class CISchemaGroup(models.Model):
    name = models.CharField("模型分组名称", max_length=32, null=False, blank=False, unique=True)
    alias = models.CharField("模型分组别名", max_length=32, default='')

    class Meta:
        verbose_name = "模型分组"


class CIFieldManager(models.Manager):
    def get_field_mapping(self, names: list, display_values=None):
        display_values = display_values or ("id", "name", "value_type")
        qs = self.filter(name__in=names).values(*display_values)
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


class CIManager(models.Manager):
    def items_exists(self, schema_id, keys):
        return CIField.objects.filter(schema_id=schema_id, name__in=keys).count() == len(keys)

    def add(self, schema_id, ci_data: dict):
        """
        ci_data: {field:value...}
        """
        with transaction.atomic():
            if not self.items_exists(schema_id, list(ci_data.keys())):
                raise Exception("创建字段不属于/或不存在")
            ci = self.create(schema_id=schema_id)
            field_mapping = CIField.objects.get_field_mapping(names=list(ci_data.keys()))
            for field, value in ci_data.items():
                value_mode = MODEL_TYPE_MAP[field_mapping[field]["value_type"]]
                value_mode.objects.create(ci_id=ci.id, field_id=field_mapping[field]["id"], value=value)
        return ci

    def modify(self, instance_id, schema_id, ci_data: dict):
        with transaction.atomic():
            if not self.items_exists(schema_id, list(ci_data.keys())):
                raise Exception("创建字段不属于/或不存在")
            ci_id = instance_id
            field_mapping = CIField.objects.get_field_mapping(names=list(ci_data.keys()))
            for field, value in ci_data.items():
                value_model = MODEL_TYPE_MAP[field_mapping[field]["value_type"]]
                value_model.objects.update_or_create(ci_id=ci_id, field_id=field_mapping[field]["id"],
                                                     defaults={"value": value})
        return ci_id


class CI(models.Model):
    schema = models.ForeignKey("CISchema", on_delete=models.CASCADE, related_name="item", db_constraint=False)
    objects = CIManager()

    class Meta:
        verbose_name = "配置项"
