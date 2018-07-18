from rest_framework import serializers, exceptions

from comum.models import Perfil


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'portaria', 'sexo', 'telefone', )