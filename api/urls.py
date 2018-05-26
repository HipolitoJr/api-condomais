from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'proprietario', views.ProprietarioViewSet)
router.register(r'unidadehabitarional', views.UnidadeHabitacionalViewSet)
router.register(r'grupohabitacional', views.GrupoHabitacionalViewSet)
router.register(r'condominio', views.CondominioViewSet)
router.register(r'taxaCondomio', views.TaxaCondominioViewSet)
router.register(r'itemtaxa', views.ItemTaxaViewSet)
router.register(r'despesa', views.DespesaViewSet)
router.register(r'tipodespesa', views.TipoDespesaViewSet)

urlpatterns =[

]