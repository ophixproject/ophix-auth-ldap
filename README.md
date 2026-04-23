# ophix-auth-ldap

LDAP / Active Directory authentication plugin for [ophix-server-base](https://github.com/ophixproject/ophix-server-base).

Activated automatically when `LDAP_SERVER_URI` is set in `.env`. Uses AD defaults:
`sAMAccountName` for user lookup, `NestedActiveDirectoryGroupType` for nested group
support. Users are auto-provisioned on first login; AD attributes are synced on every
login.

---

## Installation

```bash
pip install ophix-auth-ldap
```

---

## Configuration (`.env`)

| Variable | Default | Purpose |
| --- | --- | --- |
| `LDAP_SERVER_URI` | — | LDAP server URI — setting this activates the plugin (e.g. `ldap://dc.example.com`) |
| `LDAP_BIND_DN` | — | Bind DN for directory queries |
| `LDAP_BIND_PASSWORD` | — | Bind password |
| `LDAP_USER_SEARCH_BASE` | — | Base DN for user search (e.g. `OU=Users,DC=example,DC=com`) |
| `LDAP_STAFF_GROUP` | — | Full DN of AD group whose members get `is_staff=True` |
| `LDAP_SUPERUSER_GROUP` | — | Full DN of AD group whose members get `is_superuser=True` |
| `LDAP_REQUIRE_GROUP` | — | Full DN of AD group — only members can log in (optional) |
| `LDAP_START_TLS` | `False` | Set `True` to enable STARTTLS. Use `ldaps://` URI for direct TLS on port 636. |

Group membership is re-evaluated on every login — staff and superuser flags are kept
in sync with AD group membership automatically.

---

## Notes

- LDAP and SSO (`ophix-auth-oidc`) can be active simultaneously — LDAP handles the
  admin username/password form, SSO handles the redirect flow.
- Falls back gracefully if `django-auth-ldap` is not installed — a warning is logged
  and the plugin has no effect.
