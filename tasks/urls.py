from django.urls import path
from . import views 

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/completed', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.tasks_create, name='tasksCreate'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.task_complete, name='complete'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='delete'),
]
