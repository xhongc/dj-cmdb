from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.subscription.models import Subscription
from applications.subscription.serializers import SubscriptionSerializer
from component.drf.pagination import CustomPageNumberPagination
from component.drf.viewsets import GenericViewSet


class SubscriptionViewSets(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           GenericViewSet):
    queryset = Subscription.objects.all().order_by('-create_time')
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPageNumberPagination

    @action(methods=["post"], detail=False)
    def test(self, request, *args, **kwargs):
        print("接受到消息推送", args, kwargs)
        return Response({})
