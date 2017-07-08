from django.conf.urls import url
from user_ops import views
urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle', views.register_handle),
    url(r'^register_valid', views.register_valid),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^userinfo/$', views.userinfo),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),
    url('^logout/$',views.logout),
]
