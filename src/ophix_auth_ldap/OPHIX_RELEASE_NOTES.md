# Ophix Auth Ldap Release Notes

## 2026.10.04.01

- Reworked `README.md`'s opening with a hook-first pitch (fleet admin login staying in sync
  with the account IT already manages in Active Directory, instead of a separate one to
  provision and revoke), as part of the 16-package taskserver-release-wave README overhaul.

## 2026.09.26.02

- Verified real compatibility under Python 3.14 (not just added the classifier) as part of the taskserver-release-wave compatibility sweep, and added `Programming Language :: Python :: 3.14` to the package classifiers.

## 2026.09.26.01

- Docs: added `LDAP_GROUP_SEARCH_BASE` and `LDAP_LOG_LEVEL` to the README's
  configuration table — both are real, settable env vars that were missing
  from the docs.

## 2026.05.05.01

- Added `OPHIX_RELEASE_NOTES.md` for release notes delivery.
