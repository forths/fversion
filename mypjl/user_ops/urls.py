from django.conf.urls import url
from user_ops import views
urlpatterns = [
    url(r'^register/$', views.register),
]
