from django.urls import path
from music_app_db_viewer import views

urlpatterns = [
    path('', views.index, name='index'),
]