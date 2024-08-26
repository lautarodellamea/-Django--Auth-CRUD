from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signUp, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/tasks_completed/', views.tasksCompleted, name="tasks_completed"),
    path('logout/', views.signOut, name="logout"),
    path('signin/', views.signIn, name="signin"),
    path('tasks/create', views.createTask, name="create_task"),
    path('tasks/<int:task_id>', views.taskDetail, name="task_detail"),
    path('tasks/<int:task_id>/complete',
         views.completeTask, name="complete_task"),
    path('tasks/<int:task_id>/delete',
         views.deleteTask, name="delete_task"),
]
