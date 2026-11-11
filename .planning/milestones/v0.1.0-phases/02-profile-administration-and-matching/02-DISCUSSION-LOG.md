# Phase 2: Profile administration and matching - Discussion Log

> **Audit trail only.** Not input to planning/research/execution; use 02-CONTEXT.md.

**Date:** 2026-11-06
**Areas discussed:** Profile administration, Field selection and ordering, Filter configuration, Changes and deletion

User selected all four areas, advanced after each four-question set, and explicitly chose to create the context.

## Profile administration

### 1. Where should administrators manage profiles?

| Option | Selected |
| --- | --- |
| NetBox plugin pages | ✓ |
| Django admin only |  |
| Both |  |

**User response:** `1`
**Decision:** NetBox plugin pages: standard list/add/edit/delete pages.

### 2. Should a profile have a separate internal name and section title?

| Option | Selected |
| --- | --- |
| One title | ✓ |
| Separate name and title |  |
| Name plus optional title |  |

**User response:** `1`
**Decision:** One title identifies the profile and becomes its section heading.

### 3. Can multiple profiles share the same title?

| Option | Selected |
| --- | --- |
| Yes | ✓ |
| No; unique titles |  |

**User response:** `1`
**Decision:** Yes; duplicate titles are allowed.

### 4. What should the profile list show?

| Option | Selected |
| --- | --- |
| Configuration overview | ✓ |
| Compact list |  |

**User response:** `1`
**Decision:** Configuration overview: title, enabled state, display order, field-selection mode, readable filter summary.

## Field selection and ordering

### 1. How should administrators arrange Selected fields?

| Option | Selected |
| --- | --- |
| Drag to reorder | ✓ |
| Numeric order |  |
| Native NetBox order |  |

**User response:** `1`
**Decision:** Drag to reorder selected fields.

### 2. What order should All applicable fields follow?

| Option | Selected |
| --- | --- |
| Native NetBox order | ✓ |
| Alphabetical by label |  |
| Alphabetical by internal name |  |

**User response:** `1`
**Decision:** Native NetBox custom-field ordering.

### 3. Remember manual selection when switching to All mode?

| Option | Selected |
| --- | --- |
| Remember it | ✓ |
| Clear it |  |

**User response:** `1`
**Decision:** Remember selection and ordering; ignore in All mode and restore when switching back.

### 4. Allow Selected fields profile with no fields?

| Option | Selected |
| --- | --- |
| Require at least one field | ✓ |
| Allow an empty selection |  |

**User response:** `1`
**Decision:** Require at least one field in Selected mode.

## Filter configuration

### 1. How should applicability filters be entered?

| Option | Selected |
| --- | --- |
| Three optional selectors | ✓ |
| Add rule rows |  |

**User response:** `1`
**Decision:** Three optional searchable multi-selects: Device Type, role and tag. Empty selector adds no restriction.

### 2. How to indicate unrestricted profiles?

| Option | Selected |
| --- | --- |
| Inline notice | ✓ |
| Confirmation on save |  |

**User response:** `1`
**Decision:** Inline notice: Applies to all Devices.

### 3. Should new profiles start enabled?

| Option | Selected |
| --- | --- |
| Disabled | ✓ |
| Enabled |  |

**User response:** `1`
**Decision:** Disabled by default; explicitly enable after configuration.

### 4. Which tags should be offered?

| Option | Selected |
| --- | --- |
| All tags available for Devices | ✓ |
| Only tags currently used on Devices |  |

**User response:** `1`
**Decision:** All tags available for Devices, including tags not currently assigned to a Device.

## Changes and deletion

### 1. What happens when a selected Device Type, role or tag is deleted?

| Option | Selected |
| --- | --- |
| Disable affected profiles | ✓ |
| Block deletion |  |
| Remove value; empty criterion matches nothing |  |

**User response:** `1`
**Decision:** Disable all affected profiles for review; do not silently broaden matching.

### 2. What happens when a selected field is deleted or ceases Device applicability?

| Option | Selected |
| --- | --- |
| Remove it; disable if none remain | ✓ |
| Disable every affected profile |  |
| Block the change |  |

**User response:** `1`
**Decision:** Remove invalid selected membership; disable profile if no valid selected fields remain.

### 3. How are equal profile display orders resolved?

| Option | Selected |
| --- | --- |
| Title, then creation order | ✓ |
| Creation order only |  |

**User response:** `1`
**Decision:** Alphabetical title, then creation order (oldest first) for identical titles.

### 4. Re-enable a corrected automatically disabled profile automatically?

| Option | Selected |
| --- | --- |
| Require explicit re-enabling | ✓ |
| Re-enable automatically |  |

**User response:** `1`
**Decision:** No; corrections preserve disabled state until administrator explicitly enables it.

## Agent discretion

No explicit delegation of product decisions. Technical implementation choices remain research/planning work within the locked decisions.

## Deferred ideas

None introduced; existing phase/milestone boundaries retained.
