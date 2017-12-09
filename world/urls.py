
from django.conf.urls import url
from . import views

app_name = "world"

urlpatterns = [
    url(r'^search_select2/$', views.search_select2, name="search_select2"),
    url(r'^search/(?P<search_type>[-\w]+)/$', views.search, name="search"),
    url(r'^country/(?P<code>[-\w]+)/$', views.get_country, name="get_country"),

]
