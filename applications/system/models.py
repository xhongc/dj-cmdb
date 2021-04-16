from django.db import models


class AuditLog(models.Model):
    ADD = "add"
    DELETE = "delete"
    MODIFY = "modify"
    RUN = "run"
    OPERATE_TYPE_MAP = ((ADD, "新增"), (DELETE, "删除"), (MODIFY, "修改"), (RUN, "执行"))

    action_time = models.DateTimeField("操作时间", auto_now=True)
    user = models.CharField("操作者", max_length=64)
    obj = models.TextField("操作对象", blank=True, null=True)
    operate_type = models.CharField("操作类型", max_length=32)
    change_message = models.TextField("操作信息", blank=True)

    class Meta:
        verbose_name = "操作日志"
        ordering = ["-id"]

    @classmethod
    def simple_create(cls, user, operate_type, obj, detail=""):
        operate_type_map = dict(cls.OPERATE_TYPE_MAP)
        cls.objects.create(
            user=user,
            obj=obj,
            operate_type=operate_type,
            change_message=f"{operate_type_map[operate_type]}{obj}[{detail}]",
        )
