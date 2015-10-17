"""ltltrans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from ltltrans import views

urlpatterns = [
    url(r'^/', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^english_to_ltl$', views.english_to_ltl, name='english_to_ltl'),
    url(r'^ltl_to_english$', views.ltl_to_english, name='ltl_to_english'),
    url(r'^hello_world$', views.hello_world, name='hello_world'),
]
