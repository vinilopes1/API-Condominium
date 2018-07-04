from rest_framework import serializers, exceptions
from condominium.portaria.models import Ocorrencia, Comentario, Entrada


class ComentarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentario
        fields = ('id', 'descricao', )
        read_only_fields = ('id', )

    def create(self, validated_data):

        ocorrencia_pk = self.context.get('ocorrencia_pk')
        descricao = validated_data['descricao']

        try:
            ocorrencia = Ocorrencia.objects.get(pk=ocorrencia_pk)
            comentario = Comentario.objects.create(ocorrencia=ocorrencia, descricao=descricao)
            return comentario
        except Ocorrencia.DoesNotExist:
            raise exceptions.NotFound(detail='Ocorrencia não localizada.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível adicionar o comentários.')






class OcorrenciaSerializer(serializers.ModelSerializer):

    comentarios = ComentarioSerializer(many=True)

    class Meta:
        model = Ocorrencia
        fields = ('id', 'status', 'descricao', 'localizacao',
                  'publico', 'informante', 'comentarios')
        read_only_fields = ('id',)


class OcorrenciaSimplesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ocorrencia
        fields = ('id', 'status', 'descricao', 'localizacao',
                  'publico', 'informante')
        read_only_fields = ('id',)


class EntradaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrada
        fields = ('id', 'data', 'hora', 'descricao', 'informante', 'status', )