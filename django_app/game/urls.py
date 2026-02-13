from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('play/<int:story_id>', views.play_story, name='play_story'),
    path('stats/', views.global_stats, name='global_stats'),
    path('restart/<int:story_id>', views.restart_story, name='restart_story'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('dashboard/', views.my_stories, name='my_stories'),
    path('story/new/', views.create_story, name='create_story'),
    path('story/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('story/<int:story_id>/publish/', views.publish_story, name='publish_story'),
]

