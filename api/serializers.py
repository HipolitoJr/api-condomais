from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, ItemTaxa, Despesa, TipoDespesa


class ProprietarioSerializer(serializers.ModelSerializer):

    model = Proprietario
    fields = ('telefone',
              'usuario__first_name',
              'usuario__last_name')


class UnidadeHabitacionalSerializer(serializers.ModelSerializer):

    model = UnidadeHabitacional
    fields = ('descricao',
              'qtd_quartos',
              'ocupacao',
              'proprietario'
              'grupo_habitacional')


class GrupoHabitacionalSerializer(serializers.ModelSerializer):

    model = GrupoHabitacional
    fields = ('descricao',
              'qtd_unidades',
              'condominio')


class CondominioSerializer(serializers.ModelSerializer):

    model = Condominio
    fields = ('nome',
              'endereco',
              'cnpj')


class TaxaCondominioSerializer(serializers.ModelSerializer):

    model = TaxaCondominio
    fields = ('mes_ano',
              'data_pagamento',
              'valor_pago',
              'valor_a_pagar')


class ItemTaxaSerializer(serializers.ModelSerializer):

    model = ItemTaxa
    fields = ('descricao',
              'valor',
              'taxa_condominio')


