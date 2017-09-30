# coding: utf-8
from django.db import models
from comum.models import Base, Perfil

class Ocorrencia(Base):

    STATUS_OCORRENCIA = (
        ('resolvido', 'Resolvido'),
        ('reaberta', 'Reaberta'),
        ('finalizada', 'Finalizada'),
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Analise'),
    )

    status = models.CharField('Status', max_length=64, choices=STATUS_OCORRENCIA, default='aberta', blank=False, null=False)
    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    localizacao = models.CharField('Localizacao', max_length=128, blank=True, null=True)
    publico = models.BooleanField('Publico', default=False, blank=False, null=False)
    informante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='ocorrencias', blank=False, null=False)

    class Meta:

        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'

    def __str__(self):
        return '%s (%s)' % (self.descricao, self.informante)


class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    ocorrencia = models.ForeignKey('Ocorrencia', on_delete = models.CASCADE, related_name = 'ocorrencias', blank=False, null=False)

    class Meta:

        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.descricao


class Entrada(Base):

    STATUS_ENTRADA = (
        ('informada', 'Informada'),
        ('lida', 'Lida'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    )

    data = models.DateField('Data', blank=False, null=False)
    hora = models.TimeField('Hora', blank=True, null=True)
    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    informante = models.ForeignKey(Perfil, on_delete = models.CASCADE, related_name = 'entradas', blank=False, null=False)
    status = models.CharField('Status', max_length=64, choices=STATUS_ENTRADA, default='informada', blank=False, null=False)

    class Meta:

        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return self.descricao