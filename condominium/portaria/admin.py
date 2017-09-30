from django.contrib import admin
from portaria.models import Ocorrencia, Entrada, Comentario


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('status', 'descricao', 'informante')


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'descricao', 'informante')

    fieldsets = (
        (None, {
            'fields': ( ('data', 'hora',), 'descricao', )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.informante = request.user.perfil
        obj.save()


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'ocorrencia')