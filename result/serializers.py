from rest_framework import serializers
from data import models


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Score
        fields = '__all__'
