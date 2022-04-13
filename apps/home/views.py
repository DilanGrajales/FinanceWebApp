from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from apps.home.models import *


# Create your views here.
#  * Pagina de inicio del usuario
@login_required(login_url="/login/")
def index(request):
    transacciones = MoneyRegister.objects.filter(user=request.user)
    context = {
        'segment': 'categories',
        'transacciones': transacciones,
    }
    return render(request, 'index.html', context)


# * Registro
def registro(request, type_id):
    # Obtener usuario
    _userid = request.user.id
    usuario = User.objects.get(id=_userid)
    
    if (request.method == "POST") and ("guardar" in request.POST):
        # Obtener datos
        _date = request.POST['date']
        _amount = request.POST['amount']
        _category = request.POST['category']
        _description = request.POST['description']
        
        # Guardar registro
        MoneyRegister.objects.create(user=usuario, type=type_id, date=_date, amount=_amount, category_id=_category, description=_description)
        
        # Redireccionar
        return redirect('home')
    
    context = {'categories': Categories.objects.all()}
    
    return render(request, 'registro.html', context)
    

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
        print(context['segment'])

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    # 404 error page
    except template.TemplateDoesNotExist:
        return render(request, 'home/page-404.html', context)
    # 505 error page
    except:
        return render(request, 'home/page-500.html', context)
