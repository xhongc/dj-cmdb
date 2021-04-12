import requests
from django.dispatch import receiver

from applications.cmdb.models import CISchema
from applications.subscription.models import Subscription
from applications.subscription.signals import ci_create_signal


@receiver(ci_create_signal)
def ci_call_back(sender, **kwargs):
    print('ci change', sender, kwargs)
    schema = CISchema.objects.filter(id=kwargs["schema_id"]).first()
    sub_data = Subscription.objects.filter(meta__has_key=schema.name).values()
    for sub in sub_data:
        url = sub.get("notify_url")
        print(url)
        res = requests.post(url,
                            data={"schema_id": kwargs["schema_id"], "field_value": kwargs["field_value"]})