from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from data import models
from . import serializers


class ScoreViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer

    def get_queryset(self):
        month_start = self.request.query_params.get('monthStart')
        month_end = self.request.query_params.get('monthEnd')
        if month_start and month_end:
            return self.queryset.model.objects.filter(
                data__file_name__gte=month_start, data__file_name__lte=month_end,
                data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by('data__file_name')
        else:
            return self.queryset


class AssetsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Assets.objects.all()
    serializer_class = serializers.AssetsSerializer

    def get_queryset(self):
        queryset = models.Assets.objects.filter(data__file_name__gte=self.request.query_params['monthStart'],
                                                data__file_name__lte=self.request.query_params['monthEnd'],
                                                data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by(
            'data__file_name')
        return queryset


class ReserveViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = models.Reserve.objects.all()
    serializer_class = serializers.ReserveSerializer

    def get_queryset(self):
        queryset = models.Reserve.objects.filter(data__file_name__gte=self.request.query_params['monthStart'],
                                                 data__file_name__lte=self.request.query_params['monthEnd'],
                                                 data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by(
            'data__file_name')
        return queryset
