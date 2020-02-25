import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from alm_backend.settings import ACCOUNTS
from custom.paginations import DataPagination
from .models import Data, Account
from .serializers import DataListSerializer, DataCreateSerializer, DataUpdateSerializer


def create_or_update(serializer):
    # 把额外字段抽取出来
    indicator = serializer.validated_data.pop('indicator')
    indicator_by_acc = serializer.validated_data.pop('indicator_by_acc')
    # 保存模型实例
    serializer.save()
    # 创建或更新外键
    data = serializer.instance
    for i in indicator:
        i['model'].objects.update_or_create(data=data, defaults=i['value'])
    for acc in ACCOUNTS:
        account = Account.objects.get_or_create(pk=acc[0])[0]
        for field in indicator_by_acc:
            field['model'].objects.update_or_create(account=account, data=data, defaults=field['value'][acc[0]])


class DataViewSet(ModelViewSet):
    """
    更新量化评估表时会删除旧表
    """
    queryset = Data.objects.all()
    filter_backends = [DjangoFilterBackend]
    pagination_class = DataPagination
    filterset_fields = {
        'file_name': ['icontains']
    }

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return DataCreateSerializer
        if self.action == 'update':
            return DataUpdateSerializer
        return DataListSerializer

    def perform_create(self, serializer):
        # 给实例添加上传人
        serializer.validated_data['created_by'] = self.request.user.username
        create_or_update(serializer)

    def perform_update(self, serializer):
        # 删除旧文件
        try:
            os.remove(serializer.instance.file.path)
        except Exception as e:
            print(e)
        # 给实例添加修改人
        serializer.validated_data['modified_by'] = self.request.user.username
        create_or_update(serializer)
