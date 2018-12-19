from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^dtpage/(?P<pk>[0-9]+)?$',views.dtpage,name='dtpage' ),
    url(r'^dtpage_collection/(?P<pk>[0-9]+)?$',views.dtpage_collection,name='dtpage_collection' ),
]