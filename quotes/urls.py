from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #lo que hace esto es llamar a la funcion index del archivo views.py
    path('monday', views.monday), #lo que hace esto es llamar a la funcion monday del archivo views.py
    path('tuesday', views.tuesday),
    path('<str:day>', views.days_week, name='day-quote'), #esto lo que hace es ser url dinamica, es decir que puede recibir cualquier valor y lo envia a la funcion days_week y el parametro name sirve para identificar la url y poder usarla en otras partes de la aplicacion

    
]
