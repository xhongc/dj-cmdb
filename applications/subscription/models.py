from datetime import datetime

from django.db import models


class Subscription(models.Model):
    name = models.CharField("订阅名称", max_length=32, null=False, blank=False)
    subscriber = models.CharField("订阅者", max_length=32, null=False, blank=False)
    notify_url = models.CharField("通知url", max_length=255, null=False, blank=False)
    success_code = models.CharField("成功状态码", max_length=8, default="200")
    timeout = models.CharField("超时时间", max_length=8, default="60")
    meta = models.JSONField("订阅数据", null=False)

    create_time = models.DateTimeField("创建时间", default=datetime.now)
    update_time = models.DateTimeField("修改时间", auto_now=True)
