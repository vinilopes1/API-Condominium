from django.shortcuts import render
from rest_framework import  viewsets, authentication, permissions

from portaria.models import Ocorrencia, Comentario, Entrada
from .serializers import OcorrenciaSerializer, EntradaSerializer


class DefaultMixin(object):

    """authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
       permissions.IsAuthenticated
    )"""


class OcorrenciaViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Ocorrencia.objects.order_by('-criado_em')
    serializer_class = OcorrenciaSerializer


class EntradaViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Entrada.objects.order_by('-criado_em')
    serializer_class = EntradaSerializer