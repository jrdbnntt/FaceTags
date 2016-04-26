from django.conf.urls import url
import views

urlpatterns = [
    url(r'^user/', views.get_user, name='user'),
    url(r'^all/', views.get_all, name='all'),
    url(r'^fix/$', views.get_fix, name='fix'),
]
