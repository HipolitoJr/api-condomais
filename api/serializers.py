from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from api.models import Proprietario, UnidadeHabitacional


class ProprietarioSerializer(serializers.ModelSerializer):

    model = Proprietario
    fields = ('telefone',
              'usuario__first_name',
              'usuario__last_name')




