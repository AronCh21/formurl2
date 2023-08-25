from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('ben/', views.beneficiary, name='beneficiary'),
    path('<str:ben>/', views.sender, name='sender'),
    path('<str:ben>/<str:sender>/', views.receipt, name='receipt'),
    path('<str:ben>/<str:sender>/<str:receipt>', views.pdf, name='pdf'),
]