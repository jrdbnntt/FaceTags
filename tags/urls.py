from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test_json$', views.test_json, name='test_json'),
    url(r'^get_user/(?P<user_id>[0-9a-zA-Z]+)$', views.get_user, name='get_user')
]
