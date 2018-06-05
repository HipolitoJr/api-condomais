from django.contrib import admin

# Register your models here.
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, Despesa, \
    ItemTaxa, TipoDespesa


@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):

    list_display = ('usuario',
                    'telefone',
                    'sindico',)


@admin.register(UnidadeHabitacional)
class UnidadeHabitacionalAdmin(admin.ModelAdmin):

    list_display = ('descricao',
                    'qtd_quartos',
                    'ocupacao',
                    'proprietario',
                    'grupo_habitacional',)


@admin.register(GrupoHabitacional)
class GrupoHabitacionalAdmin(admin.ModelAdmin):

    list_display = ('descricao',
                    'qtd_unidades',
                    'condominio',)


@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):

    list_display = ('nome',
                    'cnpj',
                    'endereco',
                    'sindico',)


@admin.register(TaxaCondominio)
class TaxaCondominioAdmin(admin.ModelAdmin):

    list_display = ('mes_ano',
                    'data_vencimento',
                    'valor_pago',
                    'valor_a_pagar',
                    'unidade_habitacional',
                    'pago',)


@admin.register(ItemTaxa)
class ItemTaxaAdmin(admin.ModelAdmin):

    list_display = ('descricao',
                    'valor',
                    'despesa',
                    'taxa_condominio',)


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):

    list_display = ('valor',
                    'mes_ano',
                    'tipo_despesa',)


@admin.register(TipoDespesa)
class TipoDespesaAdmin(admin.ModelAdmin):

    list_display = ('nome',
                    'valor_rateado',)