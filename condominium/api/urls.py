from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'ocorrencias', views.OcorrenciaViewSet)
router.register(r'entradas', views.EntradaViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'avisos', views.AvisoViewSet)
router.register(r'visitantes', views.VisitanteViewSet)

urlpatterns = [
    url(r'^token/', obtain_auth_token, name='api-token'),
    url(r'^', include(router.urls)),
    url(r'^ocorrencias/(?P<pk>\d+)/comentarios/$',
        views.ComentariosViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='comentarios')
]