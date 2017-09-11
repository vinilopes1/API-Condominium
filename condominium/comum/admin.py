from django.contrib import admin
from .models import Condominio


@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'nome', 'endereco', )