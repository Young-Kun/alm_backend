from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from data import models
from . import serializers


class BaseQuarterViewSet(mixins.ListModelMixin, GenericViewSet):
    def get_queryset(self):
        month_start = self.request.query_params.get('monthStart')
        month_end = self.request.query_params.get('monthEnd')
        if month_start and month_end:
            return self.queryset.model.objects.filter(
                data__file_name__gte=month_start, data__file_name__lte=month_end,
                data__file_name__regex=r'^[0-9]{4}(0[369]|12)$').order_by('data__file_name')
        else:
            return self.queryset


class ScoreViewSet(BaseQuarterViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer


class AssetsViewSet(BaseQuarterViewSet):
    queryset = models.Assets.objects.all()
    serializer_class = serializers.AssetsSerializer


class ReserveViewSet(BaseQuarterViewSet):
    queryset = models.Reserve.objects.all()
    serializer_class = serializers.ReserveSerializer


class ModifiedDurationViewSet(BaseQuarterViewSet):
    queryset = models.ModifiedDuration.objects.all()
    serializer_class = serializers.ModifiedDurationSerializer


class CostReturnViewSet(BaseQuarterViewSet):
    queryset = models.CostReturn.objects.all()
    serializer_class = serializers.CostReturnSerializer
