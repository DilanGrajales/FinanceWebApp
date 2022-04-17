from datetime import datetime
import json
from django import template
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import View
from apps.home.models import *
from django.db import transaction
from django.db.models import *
from django.contrib import messages


# Create your views here.
#  * Pagina de inicio del usuario
@login_required(login_url="/login/")
def index(request):
    transacciones = MoneyRegister.objects.filter(user=request.user).order_by('-date')

    # ? Datos para cards de efectivo y tarjeta
    efectivo = []
    try:
        try:
            e_data = transacciones.aggregate(
                ingresos=Sum('amount', filter=Q(account=1, category__type=1))
            )

            if e_data['ingresos'] is None:
                e_data['ingresos'] = 0

            ingresos = e_data['ingresos']
            efectivo.append(ingresos)
        except:
            ingresos = 0
            efectivo.append(ingresos)

        try:
            e_data = transacciones.aggregate(
                egresos=Sum('amount', filter=Q(account=1, category__type=2))
            )

            if e_data['egresos'] is None:
                e_data['egresos'] = 0

            egresos = e_data['egresos']
            efectivo.append(egresos)
        except:
            egresos = 0
            efectivo.append(egresos)

        balance = ingresos - egresos
        efectivo.append(balance)
    except:
        balance = ingresos - egresos
        efectivo.append(balance)
    
    tarjeta = []
    try:
        try:
            e_data = transacciones.aggregate(
                ingresos=Sum('amount', filter=Q(account=2, category__type=1))
            )

            if e_data['ingresos'] is None:
                e_data['ingresos'] = 0

            ingresos = e_data['ingresos']
            tarjeta.append(ingresos)
        except:
            ingresos = 0
            tarjeta.append(ingresos)

        try:
            e_data = transacciones.aggregate(
                egresos=Sum('amount', filter=Q(account=2, category__type=2))
            )

            if e_data['egresos'] is None:
                e_data['egresos'] = 0

            egresos = e_data['egresos']
            tarjeta.append(egresos)
        except:
            egresos = 0
            tarjeta.append(egresos)

        balance = ingresos - egresos
        tarjeta.append(balance)
    except:
        balance = ingresos - egresos
        tarjeta.append(balance)

    context = {
        'segment': 'categories',
        'efectivo': efectivo,
        'tarjeta': tarjeta,
        'total': ingresos - egresos,
        'ingresos': ingresos,
        'egresos': egresos
    }
    
    return render(request, 'index.html', context)


def cuentas(request, account_id):
    hoy = datetime.date.today().strftime('%Y-%m-%d')
    
    transacciones = MoneyRegister.objects.filter(user=request.user, account=account_id).order_by('-date')
    
    for transaccion in transacciones:
        if str(transaccion.date) == hoy:
            transaccion.date = 'Hoy'
            
    context = {
        'segment': 'categories',
        'transacciones': transacciones
    }
    
    return render(request, 'cuentas.html', context)


# * Ingreso
@login_required(login_url="/login/")
@transaction.atomic()
def ingreso(request):
    if (request.method == "POST") and ("guardar" in request.POST):
        # Obtener datos
        _date = request.POST['date']
        _amount = request.POST['amount']
        _account = request.POST['account']
        _description = request.POST['description']
        
        # Asignar fecha si se deja vacio el campo
        if len(_date) == 0:
            _date = datetime.date.today().strftime('%Y-%m-%d')
        
        # Saber a donde retornar dependiendo del tipo de cuenta
        if _account == '1':
            retorno = 1
        else:
            retorno = 2
        
        with transaction.atomic():
            # Guardar registro
            MoneyRegister.objects.create(user=request.user, date=_date, account=_account, amount=_amount, category_id=_account, description=_description)
            
            # Redireccionar
            messages.success(request, 'Transaccion satisfactoria.')
            return redirect(f'tarjetas/{retorno}')
    
    context = {
        'categories': Categories.objects.filter(type=1)
    }
    
    return render(request, 'ingresos.html', context)


# * Egreso
@login_required(login_url="/login/")
@transaction.atomic()
def egreso(request):	
    if (request.method == "POST") and ("guardar" in request.POST):
        # Obtener datos
        _date = request.POST['date']
        _account = request.POST['account']
        _amount = request.POST['amount']
        _category = request.POST['category']
        _description = request.POST['description']
        
        # Asignar fecha si se deja vacio el campo
        if len(_date) == 0:
            _date = datetime.date.today().strftime('%Y-%m-%d')
        
        # Saber a donde retornar dependiendo del tipo de cuenta
        if _account == '1':
            retorno = 1
        else:
            retorno = 2
        
        with transaction.atomic():
            # Guardar registro
            MoneyRegister.objects.create(user=request.user, date=_date, account=_account, amount=_amount, category_id=_category, description=_description)
            
            # Redireccionar
            messages.success(request, 'Transaccion satisfactoria.')
            return redirect(f'tarjetas/{retorno}')
    
    context = {
        'categories': Categories.objects.filter(type=2),
    }
    
    return render(request, 'egresos.html', context)


# * Acciones
@login_required(login_url="/login/")
@transaction.atomic()
def acciones(request, id):
    registro = MoneyRegister.objects.get(id=id)
    categoria = Categories.objects.filter(type=registro.category.type).exclude(id=registro.category.id)
    
    # Editar
    if (request.method == "POST"):
        # Obtener datos
        _date = request.POST['date']
        _account = request.POST['account']
        _amount = request.POST['amount']
        _category = request.POST['category']
        _description = request.POST['description']
        
        if len(_date) == 0:
            _date = datetime.date.today().strftime('%Y-%m-%d')
        
        with transaction.atomic():
            MoneyRegister.objects.update_or_create(
                id=id,
                defaults={
                    'date': _date,
                    'account': _account,
                    'amount': _amount,
                    'category_id': _category,
                    'description': _description
                }
            )
            
            # Redimensionar
            messages.success(request, f'Se edito el registro satisfactioriamente de la categoria {registro.category.name}.')
            return redirect(reverse_lazy('cuentas', kwargs={'account_id': _account}))
    
    # Eliminar
    if (request.method == "GET" and "eliminar" in request.GET):
        with transaction.atomic():
            # Eliminar registro
            registro.delete()
            
        # Redireccionar
        messages.success(request, f'Se elimino el registro satisfactioriamente de la categoria {registro.category.name}.')
        return redirect(reverse_lazy('cuentas', kwargs={'account_id': registro.account}))

    context = {
        'registro': registro,
        'categories': categoria
    }
    
    return render(request, 'editar.html', context)


# * Pagina de Not found / Server error
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    # 404 error page
    except template.TemplateDoesNotExist:
        return render(request, 'home/page-404.html', context)
    # 505 error page
    except:
        return render(request, 'home/page-500.html', context)
    

# ? REST API
class CategoriesView(View):
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # Listar categorias
    def get(self, request, id=0):
        if id > 0:
            category = list(Categories.objects.filter(id=id).values())
            data = {'message': 'Success', 'categories': category}
        else:
            categories = list(Categories.objects.order_by('-id').values())
            if len(categories) > 0:
                data = {'message': 'Success', 'categories': categories}
            else:
                data = {'message': 'No se encontraron categorias.'}
            
        return JsonResponse(data)
    
    @transaction.atomic()
    def post(self, request):
        jd = json.loads(request.body)
        with transaction.atomic():
            Categories.objects.update_or_create(
                name=jd['name'],
                defaults={
                    'type': jd['type'],
                    'icon': jd['icon']
                }
            )
            data = {'message': 'Success'}
            
        return JsonResponse(data)
    
    def put(self, request, id):
        # ? Este metodo es solventado con el ORM de django utilizando 'update_or_create'
        pass
        
    
    def delete(self, request, id=0):
        categories = list(Categories.objects.filter(id=id).order_by('-id').values())
        if len(categories) > 0:
            Categories.objects.filter(id=id).delete()
            data = {'message': 'Success'}
        else:
            data = {'message': 'No se encontraron categorias.'}
            
        return JsonResponse(data)