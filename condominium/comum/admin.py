from django.contrib import admin
from .models import Condominio, Perfil, GrupoHabitacional, UnidadeHabitacional


@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'nome', 'endereco', 'sindico',)

    def get_queryset(self, request):
        qs = super(CondominioAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(sindico__usuario=request.user)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'sindico':
                kwargs["queryset"] = Perfil.objects.filter(condominio=request.user.perfil.condominio)
        return super(CondominioAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'telefone', 'data_nascimento', 'usuario', )

    fieldsets = (
        ("Dados", {
            'fields': ('usuario', ('telefone', 'data_nascimento',), ),
        }),
        ("Condomínio", {
            'fields': ('condominio', 'unidade_habitacional', ),
        })
    )

    def get_queryset(self, request):
        qs = super(PerfilAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(condominio=request.user.perfil.condominio)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'condominio':
                kwargs["queryset"] = Condominio.objects.filter(sindico=request.user.perfil)
        return super(PerfilAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GrupoHabitacional)
class GrupoHabitacionalAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'tipo_unidade', 'nome', 'logradouro', 'condominio', )

    fieldsets = (
        (None, {
            'fields': ('nome', ('tipo', 'tipo_unidade'), 'logradouro')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.condominio = request.user.perfil.condominio
        obj.save()

    def get_queryset(self, request):
        qs = super(GrupoHabitacionalAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(condominio__sindico__usuario=request.user)

        return qs


@admin.register(UnidadeHabitacional)
class UnidadadeHabitacionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_habitacional', 'proprietario', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'grupo_habitacional':
                kwargs["queryset"] = GrupoHabitacional.objects.filter(condominio__sindico__usuario=request.user)
        return super(UnidadadeHabitacionalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(UnidadadeHabitacionalAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(grupo_habitacional__condominio=request.user.perfil.condominio)

        return qs


