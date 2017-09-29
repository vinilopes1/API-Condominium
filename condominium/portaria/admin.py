from django.contrib import admin
from portaria.models import Ocorrencia, Entrada, Comentario


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('status', 'descricao', 'informante')


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'descricao', 'informante')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'ocorrencia')