from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('play/<int:story_id>', views.play_story, name='play_story'),
    path('stats/', views.global_stats, name='global_stats'),
    path('restart/<int:story_id>', views.restart_story, name='restart_story'),
]

