from django.contrib import admin
from portaria.models import Ocorrencia, Entrada, Comentario, Aviso, Visitante, Post


class ComentarioOcorrenciaInline(admin.TabularInline):
    model = Comentario
    fields = ('descricao', )
    extra = 1


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('status', 'descricao', )
    readonly_fields = ('informante', 'tipo', 'status')

    icon = '<i class="material-icons">assignment</i>'

    inlines = (ComentarioOcorrenciaInline,)

    def get_queryset(self, request):
        qs = super(OcorrenciaAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(informante__condominio=request.user.perfil.condominio)

        return qs

    def save_model(self, request, ocorrencia, form, change):
        if not ocorrencia.pk and not request.user.is_superuser:
            ocorrencia.tipo = 'ocorrencia'
            ocorrencia.informante = request.user.perfil
        ocorrencia.save()


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'descricao', 'informante', )

    icon = '<i class="material-icons">input</i>'

    fieldsets = (
        (None, {
            'fields': ( ('data', 'hora',), 'descricao', )
        }),
    )

    def get_queryset(self, request):
        qs = super(EntradaAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(informante__condominio=request.user.perfil.condominio)

        return qs

    def save_model(self, request, entrada, form, change):
        if not entrada.pk and not request.user.is_superuser:
            entrada.tipo = 'entrada'
            entrada.informante = request.user.perfil
        entrada.save()


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'informante',)
    readonly_fields = ('informante', )

    icon = '<i class="material-icons">notifications</i>'

    def get_queryset(self, request):
        qs = super(AvisoAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(informante__condominio=request.user.perfil.condominio)

        return qs

    def save_model(self, request, aviso, form, change):
        if not aviso.pk and not request.user.is_superuser:
            aviso.tipo = 'aviso'
            aviso.informante = request.user.perfil
        aviso.save()


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'telefone', 'data_nascimento', 'morador',)

    icon = '<i class="material-icons">directions_walk</i>'

    def get_queryset(self, request):
        qs = super(VisitanteAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(morador__condominio=request.user.perfil.condominio)

        return qs

    def save_model(self, request, visitante, form, change):
        if not visitante.pk and not request.user.is_superuser:
            visitante.morador = request.user.perfil
        visitante.save()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('status_post', 'descricao', 'atualizado_em_data_br',  'atualizado_em_hora_br', 'informante', )

    icon = '<i class="material-icons">description</i>'

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(informante__condominio=request.user.perfil.condominio)

        return qs