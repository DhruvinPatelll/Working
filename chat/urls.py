from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('room/', views.room, name='room'),
    path('room/<str:group_name>', views.room,)
]