from django.urls import path
from . import views

urlpatterns = [
    path('', views.projecs, name='projec'),
    path('project/<str:pk>', views.project, name='project'),
    path('create-projects/', views.createProject, name='create-project'),
    path('update-projects/<str:pk>/', views.updateProject, name='update-project'),
    path('delete-projects/<str:pk>/', views.deleteProject, name='delete-project')
]