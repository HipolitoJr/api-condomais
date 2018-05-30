from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, ItemTaxa, Despesa, TipoDespesa


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('username',
                  'email',
                  'password',)


class ProprietarioSerializer(serializers.ModelSerializer):

    #usuario = UserSerializer(many=False)

    class Meta:

        model = Proprietario
        fields = ('usuario',
                  'telefone',)


class UnidadeHabitacionalSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnidadeHabitacional
        fields = ('descricao',
                  'qtd_quartos',
                  'ocupacao',
                  'proprietario',
                  'grupo_habitacional',)


class GrupoHabitacionalSerializer(serializers.ModelSerializer):

    class Meta:

        model = GrupoHabitacional
        fields = ('descricao',
                  'qtd_unidades',
                  'condominio',)


class CondominioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Condominio
        fields = ('nome',
                  'endereco',
                  'cnpj',)


class TaxaCondominioSerializer(serializers.ModelSerializer):

    class Meta:

        model = TaxaCondominio
        fields = ('id',
                  'mes_ano',
                  'data_pagamento',
                  'valor_pago',
                  'valor_a_pagar',
                  'unidade_habitacional',)


class ItemTaxaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemTaxa
        fields = ('descricao',
                  'valor',
                  'taxa_condominio',)


class DespesaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Despesa
        fields = ('id',
                  'mes_ano',
                  'valor',
                  'tipo_despesa',)


class TipoDespesaSerializer(serializers.ModelSerializer):

    class Meta:

        model = TipoDespesa
        fields = ('nome',
                  'valor_rateado',)


