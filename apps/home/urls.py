from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # Inicio
    path('', views.index, name='home'),
    path('registro/<int:type_id>', views.registro, name='registro'),
    path('acciones/<int:id>', views.acciones, name='acciones'),

    # Coincidencia con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),

]
