"""Request-local, read-only presentation of native custom field values."""
from dataclasses import dataclass
from typing import Any

from .matching import get_matching_profiles, get_profile_fields


@dataclass(frozen=True)
class ParameterRow:
    field: Any
    raw_value: Any
    value: Any
    is_unset: bool
    unavailable: bool


@dataclass(frozen=True)
class ParameterSection:
    profile: Any
    rows: tuple[ParameterRow, ...]


def is_unset(field, raw_value):
    """False, zero, and empty JSON structures are meaningful native values."""
    if raw_value is None:
        return True
    if field.type == 'json':
        return False
    if field.type in ('multiselect', 'multiobject'):
        return raw_value == []
    return raw_value == ''


def resolve_reference_value(field, raw_value, user):
    """Return only native viewer-permitted instances, never deserialize raw IDs."""
    model = field.related_object_type.model_class()
    permitted = model.objects.restrict(user, 'view')
    if field.type == 'object':
        value = permitted.filter(pk=raw_value).first()
        return value, value is None
    value = tuple(permitted.filter(pk__in=raw_value))
    # Partial lists expose only allowed objects, with no hidden count or marker.
    return value, not value


def build_sections(device, user):
    """Resolve fresh native values after the caller authorizes this Device."""
    rows = {}
    sections = []
    for profile in get_matching_profiles(device):
        section_rows = []
        for field in get_profile_fields(profile):
            if field.pk not in rows:
                raw = device.custom_field_data.get(field.name)
                unset = is_unset(field, raw)
                value, unavailable = raw, False
                if not unset:
                    if field.type in ('object', 'multiobject'):
                        value, unavailable = resolve_reference_value(field, raw, user)
                    else:
                        value = field.deserialize(raw)
                rows[field.pk] = ParameterRow(field, raw, value, unset, unavailable)
            section_rows.append(rows[field.pk])
        sections.append(ParameterSection(profile, tuple(section_rows)))
    return tuple(sections)
