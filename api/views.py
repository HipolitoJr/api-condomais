from django.contrib.auth.models import User
from django.shortcuts import render
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, ItemTaxa, Despesa, TipoDespesa
from api.serializers import ProprietarioSerializer, UnidadeHabitacionalSerializer, GrupoHabitacionalSerializer, \
    CondominioSerializer, TaxaCondominioSerializer, ItemTaxaSerializer, DespesaSerializer, TipoDespesaSerializer, \
    UserSerializer, CondominioDetalhadoSerializer, GrupoHabitacionalDetalhadoSerializer, UnidadeHabitacionalDetalhadaSerializer,\
    TaxaCondominioDetalhadoSerializer
from rest_framework import authentication, permissions, viewsets

from rest_framework.response import Response
from rest_framework import viewsets, authentication, permissions, filters, status, exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProprietarioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Proprietario.objects.all()
    serializer_class = ProprietarioSerializer


class UnidadeHabitacionalViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = UnidadeHabitacional.objects.all()
    serializer_class = UnidadeHabitacionalSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UnidadeHabitacional.objects.all()

        if not user.is_superuser or user.sindico:
            minhas_unidades = user.proprietario.minhas_unidades.all()
            unidade = minhas_unidades[0]
            queryset = UnidadeHabitacional.objects.filter(grupo_habitacional__condominio__pk=unidade.grupo_habitacional.condominio.pk)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        unidade_habitacional = self.get_object()
        serializer = UnidadeHabitacionalDetalhadaSerializer(unidade_habitacional)
        return Response(serializer.data)

class GrupoHabitacionalViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = GrupoHabitacional.objects.all()
    serializer_class = GrupoHabitacionalSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = GrupoHabitacional.objects.all()

        if not user.is_superuser or user.sindico:
            minhas_unidades = user.proprietario.minhas_unidades.all()
            unidade = minhas_unidades[0]
            queryset = GrupoHabitacional.objects.filter(condominio__pk = unidade.grupo_habitacional.condominio.pk )

        elif user.is_superuser or user.sindico:
            minhas_unidades = user.proprietario.minhas_unidades.all()
            unidade = minhas_unidades[0]
            queryset = GrupoHabitacional.objects.filter(pk=unidade.grupo_habitacional.pk)

        return queryset





    def retrieve(self, request, *args, **kwargs):

        grupo_habitacional = self.get_object()
        serializer = GrupoHabitacionalDetalhadoSerializer(grupo_habitacional)
        return Response(serializer.data)

class CondominioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Condominio.objects.all();
    serializer_class = CondominioSerializer

    def retrieve(self, request  , *args, **kwargs):
        condominio = self.get_object()
        serializer = CondominioDetalhadoSerializer(condominio)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user

        queryset = Condominio.objects.all();

        if user.sindico:
            queryset = Condominio.objects.filter(sindico__pk = user.pk)
        else:
            queryset = Condominio.objects.filter(sindico__pk = user.pk)


    # def create(self, request, *args, **kwargs):
    #     if request.user.is_superuser:
    #         serializer = CondominioSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    #     return Response({"mensagem": "Você não tem permissão para criar condominios"}, status=status.HTTP_400_BAD_REQUEST)

class TaxaCondominioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = TaxaCondominio.objects.all()
    serializer_class = TaxaCondominioSerializer


    def get_queryset(self):
        user = self.request.user

        queryset = TaxaCondominio.objects.all()

        if user.proprietario.sindico:
            queryset = TaxaCondominio.objects.filter(
                unidade_habitacional__grupo_habitacional__condominio__sindico__pk = user.pk)

        elif not user.is_superuser:
             queryset = TaxaCondominio.objects.filter(unidade_habitacional__proprietario__pk = user.proprietario.pk)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        taxa_condominio = self.get_object()
        serializer = TaxaCondominioDetalhadoSerializer(taxa_condominio)
        return Response(serializer.data)



    @api_view(['PUT'])
    def registrar_pagamento(request, taxa_condominio_pk):
        try:
            dicionario_taxa = eval(request.body)
            taxa_condominio = TaxaCondominio.objects.get(pk=taxa_condominio_pk)
            taxa_condominio.valor_pago = dicionario_taxa['valor_pago']
            taxa_condominio.realizar_pagamento(dicionario_taxa['valor_pago'])
            taxa_condominio.save()
        except:
            return Response({"mensagem": "Erro ao lançar pagamento"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"mensagem": "Pagamento lançado com sucesso!"})

    @api_view(['PUT'])
    def aprovar_pagamento(request, taxa_condominio_pk):
        try:
            dicionario_taxa = eval(request.body)
            taxa_de_condominio = TaxaCondominio.objects.get(pk=taxa_condominio_pk)
            taxa_de_condominio.pago = dicionario_taxa['pago']
            taxa_de_condominio.save()
        except:
            return Response({"mensagem": "Erro ao aprovar pagamento"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"mensagem": "Pagamento aprovado com sucesso!"})

class ItemTaxaViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = ItemTaxa.objects.all()
    serializer_class = ItemTaxaSerializer


class DespesaViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer

    @api_view(['POST'])
    def distribuir_despesa_condominio(request, condominio_pk):

        try:
            dicionario_despesa = eval(request.body)
            tipo_despesa = TipoDespesa.objects.get(pk=dicionario_despesa['tipo_despesa'])
            despesa = Despesa.objects.create(mes_ano=dicionario_despesa['mes_ano'], valor=dicionario_despesa['valor'], tipo_despesa=tipo_despesa)
            condominio = Condominio.objects.get(pk=condominio_pk)
            condominio.distribuir_despesa(despesa)
        except:
            return Response({"mensagem": "Erro ao lançar a despesa"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensagem" : "Despesa lançada com sucesso!"})

    @api_view(['POST'])
    def distribuir_despesa_grupo_habitacional(request, grupo_habitacional_pk):
        try:
            dicionario_despesa = eval(request.body)
            tipo_despesa = TipoDespesa.objects.get(pk=dicionario_despesa['tipo_despesa'])
            despesa = Despesa.objects.create(mes_ano=dicionario_despesa['mes_ano'], valor=dicionario_despesa['valor'],
                                             tipo_despesa=tipo_despesa)
            grupo_habitacional = GrupoHabitacional.objects.get(pk=grupo_habitacional_pk)
            grupo_habitacional.distribuir_despesa(despesa)
        except:
            return Response({"mensagem": "Erro ao lançar a despesa"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensagem": "Despesa lançada com sucesso!"})

    @api_view(['POST'])
    def distribuir_despesa_unidade_habitacional(request, unidade_habitacional_pk):
        try:
            dicionario_despesa = eval(request.body)
            tipo_despesa = TipoDespesa.objects.get(pk=dicionario_despesa['tipo_despesa'])
            despesa = Despesa.objects.create(mes_ano=dicionario_despesa['mes_ano'], valor=dicionario_despesa['valor'],
                                             tipo_despesa=tipo_despesa)
            unidade_habitacional = UnidadeHabitacional.objects.get(pk=unidade_habitacional_pk)
            unidade_habitacional.registrar_despesa(despesa)
        except:
            return Response({"mensagem": "Erro ao lançar a despesa"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensagem": "Despesa lançada com sucesso!"})


class TipoDespesaViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = TipoDespesa.objects.all()
    serializer_class = TipoDespesaSerializer


