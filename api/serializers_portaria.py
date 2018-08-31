from rest_framework import serializers, exceptions
from portaria.models import Ocorrencia, Comentario, Entrada, Aviso, Post, Visitante

from comum.models import Perfil
from .serializers_comum import PerfilSerializer, UnidadeHabitacionalSerializer


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
    informante = PerfilSerializer(many=False, read_only=True)

    class Meta:
        model = Ocorrencia
        fields = ('id', 'status', 'descricao', 'localizacao',
                  'publico', 'informante', 'comentarios',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        print(validated_data)
        user_logado = self.context.get('logado')
        validated_data['tipo'] = 'ocorrencia'
        validated_data['informante'] = user_logado

        ocorrencia = Ocorrencia.objects.create(**validated_data)
        return ocorrencia


class OcorrenciaSimplesSerializer(serializers.ModelSerializer):

    informante = PerfilSerializer(many=False, read_only=True)

    class Meta:
        model = Ocorrencia
        fields = ('id', 'status', 'descricao', 'localizacao',
                  'publico', 'informante',  )
        read_only_fields = ('id', 'status', 'informante',)


class EntradaSerializer(serializers.ModelSerializer):

    informante = PerfilSerializer(many=False, read_only=True)

    class Meta:
        model = Entrada
        fields = ('id', 'data_entrada', 'hora_entrada', 'descricao', 'informante', 'data', 'hora', 'status',)
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

    informante = PerfilSerializer(many=False, read_only=True)

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

    informante = PerfilSerializer(many=False, read_only=True)
    foto = serializers.ImageField(max_length=None, use_url=True)


    class Meta:
        model = Post
        fields = ('id', 'descricao', 'informante', 'atualizado_em_data_br', 'atualizado_em_hora_br', 'status_post', 'tipo', 'publico', 'foto', )


class VisitanteSerializer(serializers.ModelSerializer):

    unidade_habitacional = UnidadeHabitacionalSerializer(many=False, read_only= True)
    class Meta:
        model = Visitante
        fields = ('id', 'nome', 'sexo', 'telefone', 'data_nascimento', 'unidade_habitacional', )

    def create(self, validated_data):
        user_logado = self.context.get('logado')
        validated_data['unidade_habitacional'] = user_logado.unidade_habitacional.pk

        try:
            visitante = Visitante.objects.create(**validated_data)
        except:
            raise exceptions.NotAcceptable(detail='Nao foi possivel adicionar')
        return visitante