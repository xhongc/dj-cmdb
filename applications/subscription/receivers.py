from django.dispatch import receiver

from applications.cmdb.models import CISchema
from applications.subscription.models import Subscription
from applications.subscription.signals import ci_create_signal
from component.utils.async_request import async_request

import asyncio


@receiver(ci_create_signal)
def ci_call_back(sender, **kwargs):
    schema = CISchema.objects.filter(id=kwargs["schema_id"]).first()
    sub_data = Subscription.objects.filter(meta__has_key=schema.name).values()
    request_data = {"schema_id": kwargs["schema_id"],
                    "schema_name": schema.name,
                    "field_value": kwargs["field_value"]}
    request_data_map = {}
    for sub in sub_data:
        url = sub.get("notify_url")
        request_data_map[url] = request_data
    # will be upgrade celery mode
    asyncio.run(async_request("post", request_data_map))
