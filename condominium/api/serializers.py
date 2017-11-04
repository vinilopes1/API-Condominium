from rest_framework import serializers
from portaria.models import Ocorrencia, Comentario, Entrada


class OcorrenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ocorrencia
        fields = ('id', 'status', 'descricao', 'localizacao', 'publico', 'informante', )


class EntradaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrada
        fields = ('id', 'data', 'hora', 'descricao', 'informante', 'status', )