"""alm_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from data import views as data_views
from result import views as result_views

from .settings import MEDIA_ROOT

router = DefaultRouter()
# 通用路由
router.register(r'data', data_views.DataViewSet)
router.register(r'result/score', result_views.ScoreViewSet)
router.register(r'result/assets', result_views.AssetsViewSet)
router.register(r'result/reserve', result_views.ReserveViewSet)

urlpatterns = [
    # 后台管理
    path('admin/', admin.site.urls),
    # 媒体文件
    path('media/<path:path>/', serve, {'document_root': MEDIA_ROOT}),
]

# api相关的路由
api_url_prefix = 'api/'
urlpatterns += [
    # jwt认证
    path(api_url_prefix + 'jwt-token-auth/', obtain_jwt_token),
    # api登录
    path(api_url_prefix, include('rest_framework.urls')),
    path(api_url_prefix, include(router.urls)),
]
