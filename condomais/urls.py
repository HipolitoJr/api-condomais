from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('api.urls'), name='api'),
    url(r'^api/v1/token', obtain_auth_token, name='api-token')

]
