from django.urls import re_path
from .consumers import IASInterviewConsumer

websocket_urlpatterns = [
    re_path(r'ws/interview/$', IASInterviewConsumer.as_asgi()),
]
