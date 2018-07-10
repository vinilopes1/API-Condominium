from rest_framework import serializers, exceptions
from portaria.models import Ocorrencia, Comentario, Entrada, Aviso, Post, Visitante


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


class AvisoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aviso
        fields = ('id', 'descricao', 'prioridade', )


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'descricao', 'foto')


class VisitanteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitante
        fields = ('id', 'nome', 'sexo', 'telefone', 'data_nascimento', )