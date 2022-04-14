from datetime import datetime
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from apps.home.models import *
from django.db import transaction
from django.db.models import *


# Create your views here.
#  * Pagina de inicio del usuario
@login_required(login_url="/login/")
def index(request):
    transacciones = MoneyRegister.objects.filter(user=request.user).order_by('-date')
    hoy = datetime.date.today().strftime('%Y-%m-%d')
    
    for transaccion in transacciones:
        if str(transaccion.date) == hoy:
            transaccion.date = 'Hoy'
    
    # Ingresos
    try:
        ingresos = transacciones.aggregate(total=Sum('amount', filter=Q(category__type=1)))
        if ingresos['total'] is None:
            ingresos = 0
        else:
            ingresos = ingresos['total']
    except:
        ingresos = 0
        
    # Egresos
    try:
        egresos = transacciones.aggregate(total=Sum('amount', filter=Q(category__type=2)))
        if egresos['total'] is None:
            egresos = 0
        else:
            egresos = egresos['total']
    except:
        egresos = 0
        
        
    context = {
        'segment': 'categories',
        'transacciones': transacciones,
        'total': ingresos - egresos,
        'ingresos': ingresos,
        'egresos': egresos
    }
    return render(request, 'index.html', context)



# * Ingreso
@login_required(login_url="/login/")
@transaction.atomic()
def ingreso(request):
    # Obtener usuario
    _userid = request.user.id
    usuario = User.objects.get(id=_userid)
    
    if (request.method == "POST") and ("guardar" in request.POST):
        # Obtener datos
        _date = request.POST['date']
        _amount = request.POST['amount']
        _account = request.POST['account']
        _description = request.POST['description']
        
        if len(_date) == 0:
            _date = datetime.date.today().strftime('%Y-%m-%d')
        
        try:
            with transaction.atomic():
                # Guardar registro
                MoneyRegister.objects.create(user=usuario, date=_date, account=_account, amount=_amount, category_id=_account, description=_description)
                
                # Redireccionar
                return redirect('home')
        except:
            return reverse(reverse_lazy('home'))
    
    context = {
        'categories': Categories.objects.filter(type=1)
    }
    
    return render(request, 'ingresos.html', context)


# * Registro
@login_required(login_url="/login/")
@transaction.atomic()
def egreso(request):
    # Obtener usuario
    _userid = request.user.id
    usuario = User.objects.get(id=_userid)
    
    if (request.method == "POST") and ("guardar" in request.POST):
        # Obtener datos
        _date = request.POST['date']
        _account = request.POST['account']
        _amount = request.POST['amount']
        _category = request.POST['category']
        _description = request.POST['description']
        
        if len(_date) == 0:
            _date = datetime.date.today().strftime('%Y-%m-%d')
        
        try:
            with transaction.atomic():
                # Guardar registro
                MoneyRegister.objects.create(user=usuario, date=_date, account=_account, amount=_amount, category_id=_category, description=_description)
                
                # Redireccionar
                return redirect('home')
        except:
            return reverse(reverse_lazy('home'))
    
    context = {
        'categories': Categories.objects.filter(type=2),
    }
    
    return render(request, 'egresos.html', context)


# * Acciones
@login_required(login_url="/login/")
@transaction.atomic()
def acciones(request, id):
    # ! Editar
    
    
    # Eliminar
    if (request.method == "GET" and "eliminar" in request.GET):
        with transaction.atomic():
            # Eliminar registro
            MoneyRegister.objects.get(id=id).delete()
            
            # Redireccionar
        return redirect('home')
    return redirect('home')
    


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
