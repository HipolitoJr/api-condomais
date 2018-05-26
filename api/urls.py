from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'proprietario', views.ProprietarioViewSet)
router.register(r'unidade-habitarional', views.UnidadeHabitacionalViewSet)
router.register(r'grupo-habitacional', views.GrupoHabitacionalViewSet)
router.register(r'condominio', views.CondominioViewSet)
router.register(r'taxa-condomio', views.TaxaCondominioViewSet)
router.register(r'item-taxa', views.ItemTaxaViewSet)
router.register(r'despesa', views.DespesaViewSet)
router.register(r'tipo-despesa', views.TipoDespesaViewSet)

urlpatterns =[
    url(r'^', include(router.urls)),
]