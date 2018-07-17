from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class PortariaConfig(ModuleMixin, AppConfig):
    name = 'portaria'
    icon = '<i class="material-icons">chat</i>'
    verbose_name = 'Comunicação'
