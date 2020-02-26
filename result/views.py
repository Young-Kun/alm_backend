from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from data.models import Score
from .serializers import ScoreSerializer


class ScoreViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        return Score.objects.filter(data__file_name__in=self.request.query_params.getlist('quarters[]'))
