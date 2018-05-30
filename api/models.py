from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Proprietario(models.Model):

    usuario = models.OneToOneField(User, null=False, blank=False)
    telefone = models.CharField('Telefone', max_length=255, null=False, blank=False)

    def __str__(self):
        return self.usuario.username

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Proprietario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil(sender, instance, **kwargs):
    instance.proprietario.save()

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

    def registrar_despesa(self, despesa):
        taxa = self.minhas_taxas.filter(mes_ano = despesa.mes_ano)
        item = ItemTaxa.objects.create(taxa_condominio=taxa)

        if not taxa.is_empty:
            item.despesa = despesa
            item.valor = self.calcula_valor_item_taxa()

        else:
            taxa = TaxaCondominio.objects.create(mes_ano=despesa.mes_ano)
            item = ItemTaxa.objects.create(taxa_condominio=taxa)
            item.despesa = despesa
            item.valor = self.calcula_valor_item_taxa()

        item.save()

    def calcula_valor_item_taxa(self, despesa):

        if not despesa.tipo_despesa.valor_rateado:
            return despesa.valor
        else:
            total_de_quartos = self.grupo_habitacional.total_de_quartos()
            valor_a_pagar = (despesa.valor/total_de_quartos) * self.qtd_quartos
            return valor_a_pagar

class GrupoHabitacional(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    qtd_unidades = models.IntegerField('Qtd unidades', null=False, blank=False)
    condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, related_name='grupos_habitacionais', null=False, blank=False)

    def total_de_quartos(self):
        unidades = self.unidades_habitacionais.all()
        total_quartos = 0

        for unidade in unidades:
            total_quartos += unidade.qtd_quartos

        return total_quartos

    def distribuir_despesa(self, despesa):
        unidades = self.unidades_habitacionais.all()

        for unidade in unidades:
            unidade.registrar_despesa(despesa)


class Condominio(models.Model):

    nome = models.CharField('Nome', max_length=255, null=False, blank=False)
    endereco = models.CharField('Endereco', max_length=255, null=False, blank=False)
    cnpj = models.CharField('CNPJ', max_length=255, null=False, blank=False)

    def distribuir_despesa(self, despesa):
        grupos = self.grupos_habitacionais.all()

        for grupo in grupos:
            grupo.distribuir_despesa(despesa)


class TaxaCondominio(models.Model):

    mes_ano = models.DateTimeField('Mes ano', max_length=255, null=False, blank=False)
    data_pagamento = models.DateTimeField('Data pagamento', null=True, blank=True)
    valor_pago = models.FloatField('Valor pago', null=True, blank=True)
    valor_a_pagar = models.FloatField('Valor a pagar', null=True, blank=True)
    unidade_habitacional = models.ForeignKey('UnidadeHabitacional', on_delete=models.CASCADE ,related_name='minhas_taxas', null=False, blank = False,)


class ItemTaxa(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    valor = models.FloatField('Valor', null=False, blank=False)
    taxa_condominio = models.ForeignKey(TaxaCondominio, on_delete=models.CASCADE, related_name='itens', null=False, blank=False)
    despesa = models.OneToOneField('Despesa', null=True, blank=True)


class Despesa(models.Model):

    valor = models.FloatField('Valor', null=False, blank=False)
    mes_ano = models.DateTimeField('Mes ano', null=False, blank=False)
    tipo_despesa = models.ForeignKey('TipoDespesa', on_delete=models.CASCADE, related_name='despesas', null=False, blank=False)

    def save(self):
        pass


class TipoDespesa(models.Model):

    nome = models.CharField('Nome', max_length=255, null=False, blank=False)
    valor_rateado = models.BooleanField('Valor', null=False, blank=False)
