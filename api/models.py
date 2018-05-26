from django.contrib.auth.models import User
from django.db import models

class Proprietario(models.Model):

    usuario = models.OneToOneField(User, null=False, blank=False)
    telefone = models.CharField('Telefone', max_length=255, null=False, blank=False)


class UnidadeHabitacional(models.Model):

    TIPOS_OCUPACAO = (
        ('Proprietario', 'proprietario'),
        ('Inquilino', 'inquilino'),
        ('Vazio', 'vazio'),
    )

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    qtd_quartos = models.IntegerField('Qtd quartos', null=False, blank=False)
    ocupacao = models.CharField('Ocupacao', max_length=255, choices=TIPOS_OCUPACAO, default='vazio', null=False, blank=False)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE, related_name='minhas_unidades', null=False, blank=False)
    grupo_habitacional = models.ForeignKey('GrupoHabitacional', on_delete=models.CASCADE, related_name='unidades_habitacionais', null=False, blank=False)

class GrupoHabitacional(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    qtd_unidades = models.IntegerField('Qtd unidades', null=False, blank=False)
    condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, related_name='grupos_habitacionais', null=False, blank=False)


class Condominio(models.Model):

    nome = models.CharField('Nome', max_length=255, null=False, blank=False)
    endereco = models.CharField('Endereco', max_length=255, null=False, blank=False)
    cnpj = models.CharField('CNPJ', max_length=255, null=False, blank=False)


class TaxaCondominio(models.Model):

    mes_ano = models.CharField('Mes ano', max_length=255, null=False, blank=False)
    data_pagamento = models.DateTimeField('Data pagamento', null=False, blank=False)
    valor_pago = models.FloatField('Valor pago', null=True, blank=True)
    valor_a_pagar = models.FloatField('Valor a pagar', null=True, blank=True)


class ItemTaxa(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    valor = models.FloatField('Valor', null=False, blank=False)
    taxa_condominio = models.ForeignKey(TaxaCondominio, on_delete=models.CASCADE, related_name='itens', null=False, blank=False)


class Despesa(models.Model):

    mes_ano = models.CharField('Mes ano', max_length=255, null=False, blank=False)
    valor = models.FloatField('Valor', null=False, blank=False)
    tipo_despesa = models.ForeignKey('TipoDespesa', on_delete=models.CASCADE, related_name='despesas', null=False, blank=False)


class TipoDespesa(models.Model):

    nome = models.CharField('Nome', max_length=255, null=False, blank=False)
    valor_rateado = models.BooleanField('Valor', null=False, blank=False)
