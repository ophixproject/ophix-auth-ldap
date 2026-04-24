from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OphixAuthLdapConfig(AppConfig):
    name = "ophix_auth_ldap"
    verbose_name = _("Ophix LDAP Authentication")
    default_auto_field = "django.db.models.BigAutoField"
