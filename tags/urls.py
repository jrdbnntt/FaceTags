from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_user/', views.get_user, name='get_user'),
    url(r'^get_all/', views.get_all, name='get_all')
]
