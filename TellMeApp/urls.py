
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('story_like/<int:pk>', views.story_like, name='story_like'),
    path('story_show/<int:pk>', views.story_show, name='story_show'),
    path('delete_story/<int:pk>', views.delete_story, name='delete'),

]