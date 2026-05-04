"""
ophix_auth_ldap.settings
~~~~~~~~~~~~~~~~~~~~~~~~
Plugin settings for LDAP / Active Directory authentication.

Activated when LDAP_SERVER_URI is set in the environment.
Requires django-auth-ldap (bundled as a dependency of this package).

Uses Active Directory defaults:
  - sAMAccountName for user lookup
  - NestedActiveDirectoryGroupType for nested group support
  - User attributes (first_name, last_name, email) synced on every login

LDAP and OIDC can be active simultaneously — OIDC handles browser-redirected
logins; LDAP handles the standard Django admin username/password form.

The plugin loader in ophix-server-base handles:
  AUTHENTICATION_BACKENDS_PREPEND — inserts LDAPBackend before ModelBackend,
                                    after any already-registered backends
All other uppercase keys are applied as non-destructive defaults.
"""

import logging
import os

logger = logging.getLogger(__name__)


def _bool_env(name, default=False):
    return os.getenv(name, "").lower() in ("1", "true", "yes")


LDAP_ENABLED = bool(os.getenv("LDAP_SERVER_URI", ""))

if LDAP_ENABLED:
    try:
        import ldap as _ldap
        from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType

        AUTH_LDAP_SERVER_URI = os.getenv("LDAP_SERVER_URI")
        AUTH_LDAP_BIND_DN = os.getenv("LDAP_BIND_DN", "")
        AUTH_LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD", "")

        _ldap_user_base = os.getenv("LDAP_USER_SEARCH_BASE", "")
        AUTH_LDAP_USER_SEARCH = LDAPSearch(
            _ldap_user_base,
            _ldap.SCOPE_SUBTREE,
            "(sAMAccountName=%(user)s)",
        )

        _ldap_group_base = os.getenv("LDAP_GROUP_SEARCH_BASE") or _ldap_user_base
        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
            _ldap_group_base,
            _ldap.SCOPE_SUBTREE,
            "(objectClass=group)",
        )
        AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()

        # Sync these AD attributes to the Django user on every login.
        AUTH_LDAP_USER_ATTR_MAP = {
            "first_name": "givenName",
            "last_name": "sn",
            "email": "mail",
        }
        AUTH_LDAP_ALWAYS_UPDATE_USER = True

        # Map AD group membership to Django permission flags.
        # Groups are matched by full DN — set LDAP_STAFF_GROUP and/or
        # LDAP_SUPERUSER_GROUP to the full DN of the relevant AD group.
        # Flags are re-evaluated on every login.
        _ldap_flags = {}
        _ldap_staff_group = os.getenv("LDAP_STAFF_GROUP", "")
        _ldap_superuser_group = os.getenv("LDAP_SUPERUSER_GROUP", "")
        if _ldap_staff_group:
            _ldap_flags["is_staff"] = _ldap_staff_group
        if _ldap_superuser_group:
            _ldap_flags["is_superuser"] = _ldap_superuser_group
        if _ldap_flags:
            AUTH_LDAP_USER_FLAGS_BY_GROUP = _ldap_flags

        # Optionally restrict login to members of a specific group.
        _ldap_require_group = os.getenv("LDAP_REQUIRE_GROUP", "")
        if _ldap_require_group:
            AUTH_LDAP_REQUIRE_GROUP = _ldap_require_group

        # Use STARTTLS on a plain ldap:// connection.
        # For LDAPS use ldaps:// in LDAP_SERVER_URI instead.
        if _bool_env("LDAP_START_TLS"):
            AUTH_LDAP_START_TLS = True

        # Prepend LDAPBackend before ModelBackend.
        # If OIDC is also active its backend will already be at the front;
        # LDAPBackend is inserted before ModelBackend regardless of order.
        AUTHENTICATION_BACKENDS_PREPEND = [
            "django_auth_ldap.backend.LDAPBackend"
        ]

        # Optional debug logging for django_auth_ldap.
        # Set LDAP_LOG_LEVEL=DEBUG in .env to see bind attempts, group queries,
        # and the reason for each login failure. Remove or set to WARNING in production.
        _ldap_log_level = os.getenv("LDAP_LOG_LEVEL", "").upper() or "WARNING"
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {"class": "logging.StreamHandler"},
            },
            "loggers": {
                "django_auth_ldap": {
                    "handlers": ["console"],
                    "level": _ldap_log_level,
                },
            },
        }

    except ImportError:
        logger.warning(
            "LDAP_SERVER_URI is set but django-auth-ldap is not installed. "
            "Install ophix-auth-ldap to enable LDAP authentication. "
            "Falling back to Django built-in authentication."
        )
        LDAP_ENABLED = False
