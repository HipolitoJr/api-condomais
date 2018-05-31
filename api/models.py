from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Proprietario(models.Model):

    usuario = models.OneToOneField(User, null=False, blank=False)
    telefone = models.CharField('Telefone', max_length=255, null=False, blank=False)
    sindico = models.BooleanField('sindico',default=False, null=False, blank=False )

    def __str__(self):
        return self.usuario.username

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Proprietario.objects.create(usuario=instance)
        tamanho_maximo_de_md5 = 77
        if (len(instance.password)) < tamanho_maximo_de_md5:
            instance.set_password(instance.password)
            instance.save()



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

    def __str__(self):
        return self.descricao

    def registrar_despesa(self, despesa):
        taxa = self.minhas_taxas.all().order_by('-mes_ano').first()
        valor_a_pagar = self.calcula_valor_item_taxa(despesa)

        if taxa is not None and taxa.data_pagamento > despesa.mes_ano:
            item = ItemTaxa.objects.create(descricao=despesa.tipo_despesa.nome,taxa_condominio=taxa, despesa= despesa, valor = valor_a_pagar)

        else:
            data_pagamento = self.capturar_data()
            taxa = TaxaCondominio.objects.create(mes_ano=despesa.mes_ano, unidade_habitacional=self, data_pagamento=data_pagamento)
            item = ItemTaxa.objects.create(descricao=despesa.tipo_despesa.nome,taxa_condominio=taxa, despesa=despesa, valor=valor_a_pagar)

        item.save()

    def calcula_valor_item_taxa(self, despesa):

        if not despesa.tipo_despesa.valor_rateado:
            return despesa.valor
        else:
            total_de_quartos = self.grupo_habitacional.total_de_quartos()
            valor_a_pagar = (despesa.valor/total_de_quartos) * self.qtd_quartos
            return valor_a_pagar

    def capturar_data(self):
        dia_atual = datetime.date.today().day
        mes_atual = datetime.date.today().month
        ano_atual = datetime.date.today().year

        if dia_atual > 20 and mes_atual < 12:
            return datetime.date(ano_atual,mes_atual+1,20)
        elif dia_atual > 20 and mes_atual == 12:
            return datetime.date(ano_atual+1, 1, 20)
        return datetime.date(ano_atual, mes_atual, 20)

class GrupoHabitacional(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    qtd_unidades = models.IntegerField('Qtd unidades', null=False, blank=False)
    condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, related_name='grupos_habitacionais', null=False, blank=False)

    def __str__(self):
        return self.descricao

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
    sindico = models.OneToOneField(Proprietario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

    def distribuir_despesa(self, despesa):
        grupos = self.grupos_habitacionais.all()

        for grupo in grupos:
            grupo.distribuir_despesa(despesa)


class TaxaCondominio(models.Model):

    mes_ano = models.DateField('Mes ano', max_length=255, null=False, blank=False)
    data_vencimento = models.DateField('Data pagamento', null=True, blank=True)
    valor_pago = models.FloatField('Valor pago', null=True, blank=True)
    valor_a_pagar = models.FloatField('Valor a pagar', null=True, blank=True)
    unidade_habitacional = models.ForeignKey('UnidadeHabitacional', on_delete=models.CASCADE ,related_name='minhas_taxas', null=False, blank = False,)
    pago = models.BooleanField("Pago", default=False, null=False, blank=False)

    def __str__(self):
        retorno = "Referente a: "
        retorno += str(self.mes_ano)
        return retorno

    def atualiza_valor_a_pagar(self):
        self.valor_a_pagar = 0
        self.save()
        itens = self.itens.all()
        for item in itens:
            self.valor_a_pagar += float(item.valor)

        self.save()

    def realizar_pagamento(self, valor_recebido):
        data_hoje = datetime.date.today()
        self.valor_pago = valor_recebido

        if data_hoje > self.data_vencimento:
            try:
                multa = TipoDespesa.objects.get(nome='Multa')
            except:
                multa = TipoDespesa.objects.create(nome = 'Multa', valor_rateado = False)

            despesa = Despesa.objects.create(mes_ano = datetime.date.today(), valor = self.valor_a_pagar * 0.02, tipo_despesa = multa)
            self.unidade_habitacional.registrar_despesa(despesa)

        self.save()


class ItemTaxa(models.Model):

    descricao = models.CharField('Descricao', max_length=255, null=False, blank=False)
    valor = models.FloatField('Valor', null=False, blank=False)
    taxa_condominio = models.ForeignKey(TaxaCondominio, on_delete=models.CASCADE, related_name='itens', null=False, blank=False)
    despesa = models.ForeignKey('Despesa',on_delete=models.CASCADE,related_name='itens_da_despesa', null=True, blank=True)

    def __str__(self):
        return self.descricao

@receiver(post_save, sender=ItemTaxa)
def atualiza_valor_a_pagar(sender, instance, created, **kwargs):
    item = instance
    item.taxa_condominio.atualiza_valor_a_pagar()

class Despesa(models.Model):

    valor = models.FloatField('Valor', null=False, blank=False)
    mes_ano = models.DateField('Mes ano', null=False, blank=False)
    tipo_despesa = models.ForeignKey('TipoDespesa', on_delete=models.CASCADE, related_name='despesas', null=False, blank=False)

    def __str__(self):
        return self.valor


class TipoDespesa(models.Model):

    nome = models.CharField('Nome', max_length=255, null=False, blank=False)
    valor_rateado = models.BooleanField('Valor', null=False, blank=False)

    def __str__(self):
        return self.nome
