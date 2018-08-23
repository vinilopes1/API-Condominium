from rest_framework import serializers, exceptions

from comum.models import Perfil, UnidadeHabitacional, GrupoHabitacional


class GrupoHabitacionalSerializer(serializers.ModelSerializer):

    class Meta:

        model = GrupoHabitacional
        fields = ('id', 'tipo', 'tipo_unidade','logradouro', )

class UnidadeHabitacionalSerializer(serializers.ModelSerializer):

    grupo_habitacional = GrupoHabitacionalSerializer(many=False, read_only=True)

    class Meta:

        model = UnidadeHabitacional
        fields = ('id', 'nome', 'grupo_habitacional',)

class PerfilSerializer(serializers.ModelSerializer):

    unidade_habitacional = UnidadeHabitacionalSerializer(many=False, read_only=True)

    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'sobrenome', 'portaria', 'sexo', 'telefone','unidade_habitacional', )