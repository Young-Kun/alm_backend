from rest_framework import serializers

from custom.parse_data import ExcelData
from . import models
import re


class DataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Data
        fields = ['url', 'id', 'file_name', 'file', 'file_size', 'created', 'created_by', 'modified', 'modified_by']

    def validate(self, attrs):
        file = attrs['file']
        file_size = file.size
        # 文件必须是.xlsx
        if file.name[-5:] != '.xlsx':
            raise serializers.ValidationError('请上传Excel文件(.xlsx)')
        # 文件大小不能超过20M
        if file_size > 1024 * 1024 * 20:
            raise serializers.ValidationError('上传的文件大小超过20M，请检查文件是否正确')
        attrs['file_size'] = file_size
        # 读取关键指标
        data = ExcelData(file)
        # 和账户无关的指标
        attrs['indicator'] = [
            {'model': models.Score, 'value': data.Score['score']}
        ]
        # 分账户的指标
        attrs['indicator_by_acc'] = [
            {'model': models.Assets, 'value': data.Assets},
            {'model': models.Reserve, 'value': data.Reserve},
            {'model': models.ModifiedDuration, 'value': data.ModifiedDuration},
            {'model': models.HedgeRate, 'value': data.HedgeRate},
            {'model': models.DV, 'value': data.DV},
            {'model': models.CostReturn, 'value': data.CostReturn},
            {'model': models.CostReturnStressBase, 'value': data.CostReturnStressBase},
            {'model': models.CostReturnStress1, 'value': data.CostReturnStress1},
            {'model': models.CostReturnStress2, 'value': data.CostReturnStress2},
            {'model': models.CostReturnStress3, 'value': data.CostReturnStress3},
            {'model': models.CashFlowTest, 'value': data.CashFlowTest},
        ]
        return attrs


class DataListSerializer(DataBaseSerializer):
    pass


class DataCreateSerializer(DataBaseSerializer):
    class Meta:
        model = models.Data
        fields = ['file_name', 'file', 'file_size', 'modified', 'modified_by']

    def validate(self, attrs):
        _attrs = super().validate(attrs)
        file = _attrs['file']
        file_name = _attrs['file_name']
        # 文件名必须为YYYYMM格式
        if not re.match(r'^[2-9][0-9]{3}[0-1][0-9]$', file_name):
            raise serializers.ValidationError('文件名必须为YYYYMM格式')
        # 文件名不能重复
        if models.Data.objects.filter(file_name=file_name).exists():
            raise serializers.ValidationError('文件名已存在')
        file.name = file_name + '.xlsx'
        return _attrs


class DataUpdateSerializer(DataBaseSerializer):
    class Meta:
        model = models.Data
        fields = ['file', 'file_size', 'modified', 'modified_by']

    def validate(self, attrs):
        _attrs = super().validate(attrs)
        file = _attrs['file']
        file.name = self.instance.file_name + '.xlsx'
        return _attrs
