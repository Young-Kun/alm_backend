from rest_framework import serializers
from data import models


class DataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Score
        fields = ['url', 'file_name', 'file', 'file_size', 'created', 'created_by', 'modified', 'modified_by']
