from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # Inicio
    path('', views.index, name='home'),
    path('registro/', views.registro, name='registro'),

    # Coincidencia con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),

]
