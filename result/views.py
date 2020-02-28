from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from data import models
from . import serializers


class ScoreViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer

    def get_queryset(self):
        queryset = models.Score.objects.filter(data__file_name__gte=self.request.query_params['monthStart'],
                                               data__file_name__lte=self.request.query_params['monthEnd'],
                                               data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by(
            'data__file_name')
        return queryset


class AssetsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Assets.objects.all()
    serializer_class = serializers.AssetsSerializer

    def get_queryset(self):
        queryset = models.Assets.objects.filter(data__file_name__gte=self.request.query_params['monthStart'],
                                                data__file_name__lte=self.request.query_params['monthEnd'],
                                                data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by(
            'data__file_name')
        return queryset
