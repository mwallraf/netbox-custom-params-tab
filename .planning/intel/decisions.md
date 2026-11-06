# Agreed decisions

Source: `docs/REQUIREMENTS.md`; user approved ingestion on 2026-11-06.
These are agreed product constraints, not shipped/validated functionality.

- Name: NetBox Custom Field Profiles; package `netbox-custom-field-profiles`;
  Python module `netbox_custom_field_profiles`.
- Existing NetBox custom fields only; native values remain authoritative.
- Initial scope: Devices, with one selected object type per profile.
- Multiple profiles for Devices; each matching enabled profile is a tab section.
- Separate Parameters tab, not an inline detail-page panel.
- Profile title, enabled state, section order, and ordered fields.
- Selected fields or dynamically all applicable fields.
- Duplicate fields across profiles are allowed.
- Optional Device Type, device role, and tag rules.
- AND between rules; OR between values, including any selected tag.
- No rules means all Devices match; profiles match automatically.
- One Edit Parameters page; repeated fields have one input.
- Reuse native permissions and validation; no native visibility changes.
- No nested profile grouping in the initial milestone.
- Later: other object types, multiple object types per profile, richer criteria.
