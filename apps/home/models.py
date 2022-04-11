from django.db import models
from django.contrib.auth.models import User


# Choices
category_choices = [
    (0, 'SELECCIONE'),
    (1, 'COMESTIBLES'),
    (2, 'RESTAURANTES'),
    (3, 'TRANSPORTE'),
    (4, 'SALUD'),
    (5, 'TIEMPO LIBRE'),
    (6, 'COMPRAS'),
    (7, 'REGALOS'),
    (8, 'PRESTAMOS'),
    (9, 'AHORROS'),
]

# Create your models here.
class MoneyRegister(models.Model):
    user = models.OneToOneField(User(id), on_delete=models.CASCADE, verbose_name='Usuario')
    date = models.DateField(verbose_name='Fecha')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    category = models.SmallIntegerField(choices=category_choices, verbose_name='Categoria')
    description = models.TextField(verbose_name='Descripción', unique=True)

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.category}'

    class Meta:
        db_table = 'MONEY_RECORD'
        verbose_name = 'REGISTRO DE GASTO'
        verbose_name_plural = 'REGISTRO DE GASTOS'