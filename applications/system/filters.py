import django_filters as filters

from applications.system.models import AuditLog


class AuditLogFilter(filters.FilterSet):
    class Meta:
        model = AuditLog
        fields = ["user", "obj", "operate_type", "action_time_gte", "action_time_lte"]

    user = filters.CharFilter(lookup_expr="icontains")
    obj = filters.CharFilter()
    operate_type = filters.CharFilter()
    action_time_gte = filters.CharFilter(field_name="action_time", lookup_expr="gte")
    action_time_lte = filters.CharFilter(field_name="action_time", lookup_expr="lte")
