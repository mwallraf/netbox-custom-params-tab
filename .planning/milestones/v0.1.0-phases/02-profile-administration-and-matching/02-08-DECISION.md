# Plan 02-08 — Legacy configuration retirement decision

The user explicitly replied **retire** at the blocking-human checkpoint.

Authorized scope: remove `CustomTabConfigGroup`, `CustomTabConfigField` and
`CustomTabConfig` through a reviewed native forward migration. The live inventory
contained one row in each table. No export was selected. Reversing the schema
does not restore those configuration rows.

Native custom-field definitions/settings, Device values and new profile tables
are outside the deletion scope. Keep migrations 0001 and 0002 intact.

Prerequisite `make check` passed before the checkpoint (35 helper tests and
configuration guards). Browser acceptance remains pending; this decision does
not approve or complete browser verification.
