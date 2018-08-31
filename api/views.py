from datetime import datetime

from django.shortcuts import render
from rest_framework import  viewsets, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from portaria.models import Ocorrencia, Comentario, Entrada, Aviso, Visitante, Post
from .serializers_portaria import OcorrenciaSerializer, OcorrenciaSimplesSerializer, EntradaSerializer, ComentarioSerializer, PostSerializer, AvisoSerializer, VisitanteSerializer


class DefaultMixin(object):

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
       permissions.IsAuthenticated,
    )


class OcorrenciaViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Ocorrencia.objects.order_by('-criado_em')
    serializer_class = OcorrenciaSimplesSerializer

    def retrieve(self, request, *args, **kwargs):
        ocorrencia = self.get_object()
        serializer = OcorrenciaSerializer(ocorrencia)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.perfil.portaria:
            queryset = self.filter_queryset(Ocorrencia.objects.filter(informante__condominio=request.user.perfil.condominio))
        else:
            queryset = self.filter_queryset(Ocorrencia.objects.filter(informante=request.user.perfil) or Ocorrencia.objects.filter(publico=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = OcorrenciaSerializer(data=request.data,
                                       context={'logado': request.user.perfil})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EntradaViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Entrada.objects.order_by('-criado_em')
    serializer_class = EntradaSerializer

    def list(self, request, *args, **kwargs):
        if request.user.perfil.portaria:
            queryset = self.filter_queryset(Entrada.objects.filter(informante__condominio=request.user.perfil.condominio))
        else:
            queryset = self.filter_queryset(Entrada.objects.filter(informante__unidade_habitacional=request.user.perfil.unidade_habitacional) or Entrada.objects.filter(publico=True))

        self.expirar_entradas(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = EntradaSerializer(data=request.data,
                                       context={'logado': request.user.perfil})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @api_view()
    @authentication_classes(authentication_classes=DefaultMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultMixin.permission_classes)
    def liberar_entrada(request, entrada_pk):
        try:
            entrada = Entrada.objects.get(pk=entrada_pk)
            mensagem = entrada.liberar_entrada()
            return Response({"detail": mensagem}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Entrada não encontrada"}, status=status.HTTP_404_NOT_FOUND)

    @api_view()
    @authentication_classes(authentication_classes=DefaultMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultMixin.permission_classes)
    def finalizar_entrada(request, entrada_pk):
        try:
            entrada = Entrada.objects.get(pk=entrada_pk)
            mensagem = entrada.finalizar_entrada()
            return Response({"detail": mensagem}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Entrada não encontrada"}, status=status.HTTP_404_NOT_FOUND)

    @api_view()
    @authentication_classes(authentication_classes=DefaultMixin.authentication_classes)
    @permission_classes(permission_classes=DefaultMixin.permission_classes)
    def cancelar_entrada(request, entrada_pk):
        try:
            entrada = Entrada.objects.get(pk=entrada_pk)
            mensagem = entrada.cancelar_entrada()
            return Response({"detail": mensagem}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Entrada não encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def expirar_entradas(self, entradas):
        for entrada in entradas:
            data_entrada = datetime.combine(entrada.data, entrada.hora)
            if data_entrada < datetime.now():
                entrada.expirar_entrada()


class ComentariosViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Comentario.objects.order_by('-criado_em')
    serializer_class = ComentarioSerializer

    def create(self, request, pk, *args, **kwargs):
        serializer = ComentarioSerializer(data=request.data,
                                         context={'ocorrencia_pk': pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(Comentario.objects.filter(ocorrencia__pk=pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Post.objects.order_by('atualizado_em')
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Post.objects.filter(informante__condominio=request.user.perfil.condominio).filter(informante__unidade_habitacional=request.user.perfil.unidade_habitacional) | Post.objects.filter(publico=True))\
            .order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AvisoViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Aviso.objects.order_by('-criado_em')
    serializer_class = AvisoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Aviso.objects.filter(informante__condominio=request.user.perfil.condominio))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = AvisoSerializer(data=request.data,
                                       context={'logado': request.user.perfil})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VisitanteViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Visitante.objects.order_by('-criado_em')
    serializer_class = VisitanteSerializer

    def list(self, request, *args, **kwargs):
        if request.user.perfil.portaria:
            queryset = self.filter_queryset(Visitante.objects.filter(unidade_habitacional__grupo_habitacional__condominio=request.user.perfil.condominio))
        else:
            queryset = self.filter_queryset(Visitante.objects.filter(unidade_habitacional = request.user.perfil.unidade_habitacional))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = VisitanteSerializer(data=request.data,
                                       context={'logado': request.user.perfil})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
