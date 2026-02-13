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
    path('story/<int:story_id>/edit/', views.edit_story, name='edit_story'),
    path('story/<int:story_id>/pages/', views.story_structure, name='story_structure'),
    path('story/<int:story_id>/page/new/', views.create_page, name='create_page'),
    path('page/<int:page_id>/edit/', views.edit_page, name='edit_page'),
    path('page/<int:page_id>/choice/add/', views.add_choice, name='add_choice'),
    path('choice/<int:choice_id>/delete/', views.delete_choice_view, name='delete_choice'),
    path('page/<int:page_id>/delete/', views.delete_page_view, name='delete_page'),
    path('story/<int:story_id>/set_start/<int:page_id>/', views.set_start_page, name='set_start_page'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
]

