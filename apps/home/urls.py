from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    # Inicio
    path('', views.index, name='home'),
    path('tarjetas/<int:account_id>', views.cuentas, name='cuentas'),
    path('tarjetas/acciones/<int:id>', views.acciones, name='acciones'),
    path('ingreso', views.ingreso, name='ingreso'),
    path('egreso', views.egreso, name='egreso'),
    # ? --------------------------------- REST API ---------------------------------
    path('api/categorias', views.CategoriesView.as_view(), name='categorias_list'),
    path('api/categorias/<int:id>', views.CategoriesView.as_view(), name='categorias_process'),

    # Coincidencia con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),

]
