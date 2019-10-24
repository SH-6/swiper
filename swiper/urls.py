"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from user import api as user_api

urlpatterns = [
    url(r'^api/user/get_vcode', user_api.get_vcode),
    url(r'^api/user/submit_vcode', user_api.submit_vcode),

    url(r'^api/user/weibo/auth', user_api.weibo_authorize),
    url(r'^api/user/weibo/callback', user_api.wb_callback),

]
