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

    comentarios = ComentarioSerializer(many=True, read_only=True)

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

    def create(self, validated_data):
        user_logado = self.context.get('logado')
        validated_data['tipo'] = 'ocorrencia'
        validated_data['informante'] = user_logado

        ocorrencia = Ocorrencia.objects.create(**validated_data)
        return ocorrencia


class EntradaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrada
        fields = ('id', 'data', 'hora', 'descricao', 'informante', 'status', )
        read_only_fields = ('informante', 'status')

    def create(self, validated_data):
        user_logado = self.context.get('logado')
        validated_data['tipo'] = 'entrada'
        validated_data['informante'] = user_logado

        try:
            entrada = Entrada.objects.create(**validated_data)
        except:
            raise exceptions.NotAcceptable(detail='Nao foi possivel adicionar.')
        return entrada


class AvisoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aviso
        fields = ('id', 'descricao', 'prioridade', 'informante', )
        read_only_fields = ('id', 'informante', )

    def create(self, validated_data):
        user_logado = self.context.get('logado')
        validated_data['informante'] = user_logado

        try:
            aviso = Aviso.objects.create(**validated_data)
        except:
            raise exceptions.NotAcceptable(detail='Nao foi possivel adicionar.')
        return aviso


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'descricao', 'publico', 'foto')


class VisitanteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visitante
        fields = ('id', 'nome', 'sexo', 'telefone', 'data_nascimento', 'morador', )

    def create(self, validated_data):
        user_logado = self.context.get('logado')
        validated_data['morador'] = user_logado

        try:
            visitante = Visitante.objects.create(**validated_data)
        except:
            raise exceptions.NotAcceptable(detail='Nao foi possivel adicionar.')
        return visitante