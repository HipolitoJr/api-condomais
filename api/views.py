from django.contrib.auth.models import User
from django.shortcuts import render
from api.models import Proprietario, UnidadeHabitacional, GrupoHabitacional, Condominio, TaxaCondominio, ItemTaxa, Despesa, TipoDespesa
from api.serializers import ProprietarioSerializer, UnidadeHabitacionalSerializer, GrupoHabitacionalSerializer, \
    CondominioSerializer, TaxaCondominioSerializer, ItemTaxaSerializer, DespesaSerializer, TipoDespesaSerializer, \
    UserSerializer
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

class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProprietarioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Proprietario.objects.all()
    serializer_class = ProprietarioSerializer

class UnidadeHabitacionalViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = UnidadeHabitacional.objects.all()
    serializer_class = UnidadeHabitacionalSerializer

class GrupoHabitacionalViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = GrupoHabitacional.objects.all()
    serializer_class = GrupoHabitacionalSerializer

class CondominioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Condominio.objects.all();
    serializer_class = CondominioSerializer

    @api_view(['POST'])
    def distribuir_despesa(request, condominio_pk):
        print(request.body)
        disc = eval(request.body)
        print(disc['mes_ano'])
        print(condominio_pk)
        tipo_despesa = TipoDespesa.objects.filter(pk=disc['tipo_despesa'])
        print(tipo_despesa[0])
        objeto = Despesa.objects.create(mes_ano=disc['mes_ano'], valor= disc['valor'], tipo_despesa=tipo_despesa[0])
        print(objeto.id)
        # condominio = Condominio.Objects.get(pk=condominio_pk)
        # condominio.distribuir_despesa(despesa)
        return Response({"mensagem": "Job reaberto!"}, status=status.HTTP_200_OK)

class TaxaCondominioViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = TaxaCondominio.objects.all()
    serializer_class = TaxaCondominioSerializer

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


