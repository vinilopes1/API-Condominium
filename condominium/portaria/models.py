# coding: utf-8
from django.db import models
from comum.models import Base, Perfil


class Post(Base):

    TIPO_POST = (
        ('ocorrencia', 'Ocorrencia'),
        ('aviso', 'Aviso'),
        ('entrada', 'Entrada'),
    )

    tipo = models.CharField('Tipo', max_length=64, choices=TIPO_POST, blank=False, null=False)
    publico = models.BooleanField('Publico', default=False, blank=False, null=False)
    informante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='ocorrencias', blank=False, null=False)

    descricao = models.CharField('Descricao', max_length=256, blank=True, null=True)
    foto = models.CharField('Foto', max_length=256, blank=True, null=True)

    class Meta:

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Ocorrencia(Post):

    STATUS_OCORRENCIA = (
        ('resolvido', 'Resolvido'),
        ('reaberta', 'Reaberta'),
        ('finalizada', 'Finalizada'),
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Analise'),
    )

    status = models.CharField('Status', max_length=64, choices=STATUS_OCORRENCIA, default='aberta', blank=False, null=False)
    localizacao = models.CharField('Localizacao', max_length=128, blank=True, null=True)

    class Meta:

        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'

    def __str__(self):
        return '%s (%s)' % (self.descricao, self.informante)


class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    ocorrencia = models.ForeignKey('Ocorrencia', on_delete = models.CASCADE, related_name = 'comentarios', blank=False, null=False)

    class Meta:

        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.descricao


class Entrada(Post):

    STATUS_ENTRADA = (
        ('informada', 'Informada'),
        ('lida', 'Lida'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    )

    data = models.DateField('Data', blank=False, null=False)
    hora = models.TimeField('Hora', blank=True, null=True)
    status = models.CharField('Status', max_length=64, choices=STATUS_ENTRADA, default='informada', blank=False, null=False)

    class Meta:

        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return self.descricao


class Aviso(Post):

    PRIORIDADE_AVISO = (
        ('baixa', 'Baixa'),
        ('razoavel', 'Razoavel'),
        ('urgente', 'Urgente'),
    )

    prioridade = models.CharField('Prioridade', choices=PRIORIDADE_AVISO, default='razoavel', max_length=256, blank=False, null=False)

    class Meta:

        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'

    def __str__(self):
        return self.descricao


class Visitante(Base):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    nome = models.CharField('Nome', max_length=256, blank=False, null=False)
    sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
    telefone = models.CharField('Telefone', max_length=16, blank=False, null=False)
    data_nascimento = models.DateField('Data de nascimento', blank=False, null=False)

    morador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='visitantes', blank=False, null=False)

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return self.nome