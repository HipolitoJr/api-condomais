from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, ItemTaxa, Despesa, TipoDespesa


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',)


class ProprietarioSerializer(serializers.ModelSerializer):

    #usuario = UserSerializer(many=False)

    class Meta:

        model = Proprietario
        fields = ('id',
                  'usuario',
                  'telefone',
                  'sindico',)


class UnidadeHabitacionalSerializer(serializers.ModelSerializer):

    class Meta:

        model = UnidadeHabitacional
        fields = ('id',
                  'descricao',
                  'qtd_quartos',
                  'ocupacao',
                  'proprietario',
                  'grupo_habitacional',)

class GrupoHabitacionalSerializer(serializers.ModelSerializer):

    class Meta:

        model = GrupoHabitacional
        fields = ('id',
                  'descricao',
                  'qtd_unidades',
                  'condominio',)

class GrupoHabitacionalDetalhadoSerializer(serializers.ModelSerializer):
    unidades_habitacionais = UnidadeHabitacionalSerializer(many=True, read_only= True)
    class Meta:

        model = GrupoHabitacional
        fields = ('id',
                  'descricao',
                  'qtd_unidades',
                  'condominio',
                  'unidades_habitacionais',)

class CondominioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Condominio
        fields = ('id',
                  'nome',
                  'endereco',
                  'cnpj',
                  'sindico',)

class CondominioDetalhadoSerializer(serializers.ModelSerializer):
    grupos_habitacionais = GrupoHabitacionalSerializer(many= True, read_only=True)
    class Meta:

        model = Condominio
        fields = ('id',
                  'nome',
                  'endereco',
                  'cnpj',
                  'sindico',
                  'grupos_habitacionais',)


class ItemTaxaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemTaxa
        fields = ('id',
                  'descricao',
                  'valor',
                  'taxa_condominio',)


class TaxaCondominioSerializer(serializers.ModelSerializer):

    class Meta:

        model = TaxaCondominio

        fields = ('id',
                  'mes_ano',
                  'data_vencimento',
                  'valor_pago',
                  'valor_a_pagar',
                  'unidade_habitacional',
                  'pago',)

        read_only_fields = ('id',
                            'pago',)


class TaxaCondominioDetalhadoSerializer(serializers.ModelSerializer):
    itens = ItemTaxaSerializer(many=True, read_only=True)

    class Meta:

        model = TaxaCondominio

        fields = ('id',
                  'mes_ano',
                  'data_vencimento',
                  'valor_pago',
                  'valor_a_pagar',
                  'unidade_habitacional',
                  'pago',
                  'itens',)

        read_only_fields = ('id',
                            'pago',)

class UnidadeHabitacionalDetalhadaSerializer(serializers.ModelSerializer):
    minhas_taxas = TaxaCondominioSerializer(many=True, read_only=True)

    class Meta:

        model = UnidadeHabitacional
        fields = ('id',
                  'descricao',
                  'qtd_quartos',
                  'ocupacao',
                  'proprietario',
                  'grupo_habitacional',
                  'minhas_taxas',)


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
        fields = ('id',
                  'nome',
                  'valor_rateado',)


