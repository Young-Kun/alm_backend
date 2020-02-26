from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from data.models import Score
from .serializers import ScoreSerializer


class ScoreViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'data__file_name': ['icontains']
    }
