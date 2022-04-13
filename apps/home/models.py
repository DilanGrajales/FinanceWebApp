import datetime
from operator import iconcat
from django.db import models
from django.contrib.auth.models import User


# Choices
type_choices = [
    (1, 'INGRESO'),
    (2, 'EGRESO'),
]


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    type = models.SmallIntegerField(choices=type_choices, verbose_name='Tipo', default=0)
    icon = models.CharField(max_length=100, verbose_name='Icono')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'CATEGORY_CAT'
        verbose_name = 'CATEGORIA'
        verbose_name_plural = 'CATEGORIAS'


class MoneyRegister(models.Model):
    user = models.ForeignKey(User(id), on_delete=models.CASCADE, verbose_name='Usuario')
    date = models.DateField(verbose_name='Fecha')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Categoria')
    description = models.TextField(verbose_name='Descripción', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.category}'

    class Meta:
        db_table = 'MONEY_RECORD'
        verbose_name = 'REGISTRO DE GASTO'
        verbose_name_plural = 'REGISTRO DE GASTOS'