from django.db import models
from django.contrib.auth.models import User

"""
Sobre organizaçaõ de Código e PEP-8: utilizar o Python
classes, semanticamente organizadas
 > choices
 > models fields
 > class Meta
 > override methods (save, clean)
 > property
 > business methods
 
"""


class Base(models.Model):

    criado_em = models.DateTimeField('Criado em', auto_now_add=True, blank=False, null=False)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)


class Condominio(Base):

    cnpj = models.CharField('CNPJ', max_length=11)
    nome = models.CharField('Nome', max_length=128, unique=True, blank=False, null=False)
    endereco = models.CharField('Endereco', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'Condominio'
        verbose_name_plural = 'Condominios'
        #unique_together = (('attr1', 'attr2'), )
        ordering = ('nome', )


class GrupoHabitacional(Base):

    TIPO_GRUPO_HABITACIONAL = (
        ('quadra', u'Quadra'),
        ('bloco', u'Bloco'),
        ('torre', u'Torre')
    )

    TIPO_UNIDADE_HABITACIONAL = (
        ('apartamento', u'Apartamento'),
        ('casa', u'Casa'),
        ('chale', u'Chale'),
    )

    nome = models.CharField('Nome', max_length=64, blank=False, null=False)
    tipo = models.CharField('Tipo', choices=TIPO_GRUPO_HABITACIONAL, blank=False, null=False)
    tipo_unidade = models.CharField('Tipo unidade', choices=TIPO_UNIDADE_HABITACIONAL, blank=False, null=False)
    logradouro = models.CharField('Logradouro', max_length=256, blank=True, null=True)

    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name='grupos_habitacionais', null=False,)

    class Meta:
        verbose_name = 'Grupo Habitacional'
        verbose_name_plural = 'Grupos Habitacionais'
        ordering = ('nome', )
        unique_together = (('nome', 'codominio'),)


class UnidadeHabitacional(Base):

    nome = models.CharField(max_length=16, blank=False, null=False)

    grupo_habitacional = models.ForeignKey(GrupoHabitacional, related_name='unidades', blank=False, null=False)
    proprietario = models.ForeignKey('Perfil', related_name='unidades', blank=False, null=False)

    class Meta:
        verbose_name = 'Unidade habitacional'
        verbose_name_plural = 'Unidades habitacionais'
        ordering = ('nome', )
        unique_together = (('nome', 'grupo_habitacional'),)



class Perfil(Base):

    SEXO = (('M', u'Masculino'), ('F', u'Feminino'))

    sexo = models.CharField('Sexo', choices=SEXO, blank=False, null=False)
    telefone = models.CharField('Telefone', max_length=20, blank=False, null=False)
    data_nascimento = models.DateTimeField('Data de nascimento', blank=False, null=False)
    foto = models.CharField(max_length=200)
    unidade_habitacional = models.ForeignKey(UnidadeHabitacional, blank=False, null=False, related_name= 'moradores')

    usuario = models.OneToOneField(User, related_name='perfil')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        #ordering = ('usuario.username')









