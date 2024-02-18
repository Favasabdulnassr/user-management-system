from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.Signup, name = 'signup'),
    path('logged/', views.Logged, name='logged'),
    path('table/', views.table, name = 'table' ),
    path('add', views.Add, name = 'add'),
    # path('edit', views.Edit, name = 'edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>', views.Delete, name='delete'),
    path('logout/', views.Logout, name='logout'),
    path('adminlogin/', views.Adminlogin, name='adminlogin'),
    path('search/', views.search, name='search')



 ]
