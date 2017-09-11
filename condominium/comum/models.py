from django.db import models

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
