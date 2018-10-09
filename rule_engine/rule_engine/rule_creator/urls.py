from django.conf.urls import url
from .url_controller import *

urlpatterns = [
    url(r'^encode/$', EncodeUrl.as_view()),
    url(r'^decode/$', DecodeUrl.as_view()),
]