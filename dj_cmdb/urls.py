from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.routers import DefaultRouter

from applications.cmdb.views import CISchemaViewSet, CIFieldViewSet, CIViewSet, CISchemaGroupViewSet
from applications.relation.views import RelationViewSet, TopoViewSets
from applications.subscription.views import SubscriptionViewSets

router = DefaultRouter()
router.register(r"ci_schema", CISchemaViewSet, basename="ci_schema")
router.register(r"ci_field", CIFieldViewSet, basename="ci_field")
router.register(r"ci", CIViewSet, basename="ci")
router.register(r"relation", RelationViewSet, basename="relation")
router.register(r"ci_schema_group", CISchemaGroupViewSet, basename="ci_schema_group")
router.register(r"subscription", SubscriptionViewSets, basename="subscription")
router.register(r"topo", TopoViewSets, basename="topo")

schema_view = get_schema_view(
    openapi.Info(
        title="API接口文档",  # 必传
        default_version='v1',  # 必传
        description="这是一个接口文档",
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/", include(router.urls)),
]
# 调试模式才显示
if settings.DEBUG:
    urlpatterns += [
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
