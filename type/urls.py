from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [

    url(r'^type_home/',views.type_home,name='type_home' ),
    url(r'^type_home_content/(?P<pk>[0-9]+)?',views.type_home_content,name='type_home_content' ),
]
