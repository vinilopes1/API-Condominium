from django.contrib import admin
from .models import Condominio, Perfil, GrupoHabitacional, UnidadeHabitacional


@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'nome', 'endereco', )


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('sexo', 'telefone', 'data_nascimento', 'foto', 'unidade_habitacional', 'usuario', )


@admin.register(GrupoHabitacional)
class GrupoHabitacionalAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'tipo_unidade', 'nome', 'logradouro', 'condominio', )


@admin.register(UnidadeHabitacional)
class UnidadadeHabitacionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_habitacional', 'proprietario', )


