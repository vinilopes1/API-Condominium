from django.contrib import admin
from condominium.portaria.models import Ocorrencia, Entrada, Comentario


class ComentarioOcorreniaInline(admin.TabularInline):
    model = Comentario
    fields = ('descricao', )
    extra = 1


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('status', 'descricao', 'informante', )

    inlines = (ComentarioOcorreniaInline, )


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'descricao', 'informante', )

    fieldsets = (
        (None, {
            'fields': ( ('data', 'hora',), 'descricao', )
        }),
    )

    def save_model(self, request, entrada, form, change):
        if not entrada.pk and not request.user.is_superuser:
            entrada.informante = request.user.perfil
        entrada.save()
