"""Native lifecycle contracts: cleanup owns plugin configuration only."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.test import TestCase
from dcim.models import Device, DeviceRole, DeviceType, Site
from extras.choices import CustomFieldStatusChoices
from extras.models import CustomField, Tag

from netbox_custom_field_profiles.forms import CustomFieldProfileForm
from netbox_custom_field_profiles.matching import get_matching_profiles, get_profile_fields
from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_tracer


class ProfileLifecycleTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)

    def profile(self, mode='all', **kwargs):
        return CustomFieldProfile.objects.create(title='Lifecycle', content_type=self.device_ct,
                                                enabled=True, field_mode=mode, **kwargs)

    def field(self, name):
        field = CustomField.objects.create(name=name, type='text')
        field.object_types.add(self.device_ct)
        return field

    def membership(self, profile, field):
        return ProfileField.objects.create(profile=profile, field=field)

    def targets(self, kind, suffix):
        if kind == 'device_types':
            return [DeviceType.objects.create(manufacturer=self.device.device_type.manufacturer,
                                             model=f'Unused {suffix}{i}', slug=f'unused-{suffix}{i}')
                    for i in range(2)]
        if kind == 'device_roles':
            return [DeviceRole.objects.create(name=f'Unused {suffix}{i}', slug=f'unused-{suffix}{i}')
                    for i in range(2)]
        return [Tag.objects.create(name=f'Unused {suffix}{i}', slug=f'unused-{suffix}{i}')
                for i in range(2)]

    def test_filter_target_deletion_matrix(self):
        for kind in ('device_types', 'device_roles', 'applicability_tags'):
            for queryset in (False, True):
                with self.subTest(kind=kind, queryset=queryset):
                    first, remaining = self.targets(kind, kind + str(queryset))
                    profiles = [self.profile(), self.profile()]
                    unrelated = self.profile()
                    for profile in profiles:
                        getattr(profile, kind).set([first, remaining])
                    target_pk = first.pk
                    if queryset:
                        type(first).objects.filter(pk=target_pk).delete()
                    else:
                        first.delete()
                    self.assertFalse(type(first).objects.filter(pk=target_pk).exists())
                    for profile in profiles:
                        profile.refresh_from_db()
                        self.assertFalse(profile.enabled)
                        self.assertEqual(list(getattr(profile, kind).all()), [remaining])
                        self.assertNotIn(profile, get_matching_profiles(self.device))
                    unrelated.refresh_from_db()
                    self.assertTrue(unrelated.enabled)

    def test_filter_deletion_rollback_and_explicit_reenable(self):
        first, remaining = self.targets('applicability_tags', 'rollback')
        profile = self.profile()
        profile.applicability_tags.set([first, remaining])
        first_pk = first.pk
        with self.assertRaises(RuntimeError), transaction.atomic():
            Tag.objects.filter(pk=first_pk).delete()
            profile.refresh_from_db()
            self.assertFalse(profile.enabled)
            raise RuntimeError('rollback')
        profile.refresh_from_db()
        self.assertTrue(profile.enabled)
        self.assertTrue(Tag.objects.filter(pk=first_pk).exists())
        Tag.objects.filter(pk=first_pk).delete()
        profile.applicability_tags.clear()
        profile.refresh_from_db()
        self.assertFalse(profile.enabled)
        form = CustomFieldProfileForm(data={
            'title': profile.title, 'content_type': self.device_ct.pk, 'display_order': 10,
            'field_mode': 'all', 'enabled': True,
        }, instance=profile)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        profile.refresh_from_db()
        self.assertTrue(profile.enabled)

    def test_intentional_rule_removal_does_not_disable(self):
        first, _ = self.targets('applicability_tags', 'intentional')
        profile = self.profile()
        profile.applicability_tags.add(first)
        profile.applicability_tags.clear()
        profile.refresh_from_db()
        self.assertTrue(profile.enabled)

    def test_each_filter_target_deletion_rolls_back_with_profile_state(self):
        for kind in ('device_types', 'device_roles', 'applicability_tags'):
            with self.subTest(kind=kind):
                target, _ = self.targets(kind, kind + 'transaction')
                profile = self.profile()
                getattr(profile, kind).add(target)
                with self.assertRaises(RuntimeError), transaction.atomic():
                    type(target).objects.filter(pk=target.pk).delete()
                    profile.refresh_from_db()
                    self.assertFalse(profile.enabled)
                    raise RuntimeError('rollback')
                profile.refresh_from_db()
                self.assertTrue(profile.enabled)
                self.assertTrue(getattr(profile, kind).filter(pk=target.pk).exists())

    def test_field_deletion_partial_last_and_all_modes(self):
        for queryset in (False, True):
            with self.subTest(queryset=queryset):
                removed = self.field('removed_' + str(queryset))
                retained = self.field('retained_' + str(queryset))
                partial, last, all_fields, unrelated = [self.profile(mode) for mode in
                                                       ('selected', 'selected', 'all', 'selected')]
                for profile in (partial, last, all_fields):
                    self.membership(profile, removed)
                self.membership(partial, retained)
                self.membership(unrelated, retained)
                before_unrelated = CustomField.objects.filter(pk=retained.pk).values().get()
                Device.objects.filter(pk=self.device.pk).update(custom_field_data={
                    'tracer_value': 'external value', retained.name: 'unchanged', removed.name: 'native cleanup',
                })
                if queryset:
                    CustomField.objects.filter(pk=removed.pk).delete()
                else:
                    removed.delete()
                for profile in (partial, last, all_fields, unrelated):
                    profile.refresh_from_db()
                self.assertTrue(partial.enabled)
                self.assertFalse(last.enabled)
                self.assertTrue(all_fields.enabled)
                self.assertTrue(unrelated.enabled)
                self.assertEqual(get_profile_fields(partial), [retained])
                self.assertFalse(last.profile_fields.exists())
                self.assertFalse(all_fields.profile_fields.exists())
                self.assertEqual(CustomField.objects.filter(pk=retained.pk).values().get(), before_unrelated)
                self.device.refresh_from_db()
                self.assertEqual(self.device.custom_field_data['tracer_value'], 'external value')
                self.assertEqual(self.device.custom_field_data[retained.name], 'unchanged')

    def test_deferred_field_deletion_cleans_before_physical_purge(self):
        field = self.field('deferred_delete')
        profile = self.profile('selected')
        self.membership(profile, field)
        with patch.object(CustomField, '_exceeds_inline_limit', return_value=True):
            field.delete()
        field.refresh_from_db()
        self.assertEqual(field.status, CustomFieldStatusChoices.STATUS_DELETING)
        self.assertFalse(profile.profile_fields.exists())
        profile.refresh_from_db()
        self.assertFalse(profile.enabled)
        # A worker replay of deletion signals must be harmless.
        from django.db.models.signals import pre_delete
        pre_delete.send(sender=CustomField, instance=field, using='default', origin=field)
        profile.refresh_from_db()
        self.assertFalse(profile.enabled)

    def test_field_deletion_rollback_and_registration_replay(self):
        from netbox_custom_field_profiles.signals import register, remove_field_memberships

        register()
        register()
        field = self.field('field_rollback')
        profile = self.profile('selected')
        self.membership(profile, field)
        with self.assertRaises(RuntimeError), transaction.atomic():
            CustomField.objects.filter(pk=field.pk).delete()
            profile.refresh_from_db()
            self.assertFalse(profile.enabled)
            self.assertFalse(profile.profile_fields.exists())
            raise RuntimeError('rollback')
        profile.refresh_from_db()
        self.assertTrue(profile.enabled)
        self.assertTrue(CustomField.objects.filter(pk=field.pk).exists())
        self.assertTrue(profile.profile_fields.filter(field=field).exists())
        remove_field_memberships([field.pk], 'default')
        remove_field_memberships([field.pk], 'default')
        profile.refresh_from_db()
        self.assertFalse(profile.enabled)

    def test_applicability_remove_clear_set_both_directions(self):
        site_ct = ContentType.objects.get_for_model(Site)
        for reverse in (False, True):
            for action in ('remove', 'clear', 'set'):
                with self.subTest(reverse=reverse, action=action):
                    field = self.field(f'applicability_{reverse}_{action}')
                    field.object_types.add(site_ct)
                    profile = self.profile('selected')
                    self.membership(profile, field)
                    if reverse:
                        manager = self.device_ct.custom_fields
                        if action == 'remove':
                            manager.remove(field)
                        elif action == 'clear':
                            manager.clear()
                        else:
                            manager.set(list(manager.exclude(pk=field.pk)))
                    else:
                        manager = field.object_types
                        if action == 'remove':
                            manager.remove(self.device_ct)
                        elif action == 'clear':
                            manager.clear()
                        else:
                            manager.set([site_ct])
                    self.assertFalse(field.object_types.filter(pk=self.device_ct.pk).exists())
                    self.assertFalse(profile.profile_fields.exists())
                    profile.refresh_from_db()
                    self.assertFalse(profile.enabled)

    def test_unrelated_type_removal_and_noop_set_keep_selection(self):
        field = self.field('still_device')
        site_ct = ContentType.objects.get_for_model(Site)
        field.object_types.add(site_ct)
        profile = self.profile('selected')
        self.membership(profile, field)
        field.object_types.remove(site_ct)
        field.object_types.set([self.device_ct])
        site_ct.custom_fields.remove(field)
        profile.refresh_from_db()
        self.assertTrue(profile.enabled)
        self.assertEqual(get_profile_fields(profile), [field])

    def test_applicability_partial_all_rollback_and_no_reenable(self):
        removed, retained = self.field('rollback_applicability'), self.field('kept_applicability')
        selected, all_fields = self.profile('selected'), self.profile('all')
        retained_before = CustomField.objects.filter(pk=retained.pk).values().get()
        for profile in (selected, all_fields):
            self.membership(profile, removed)
        self.membership(selected, retained)
        with self.assertRaises(RuntimeError), transaction.atomic():
            removed.object_types.clear()
            self.assertFalse(selected.profile_fields.filter(field=removed).exists())
            raise RuntimeError('rollback')
        self.assertTrue(selected.profile_fields.filter(field=removed).exists())
        removed.object_types.clear()
        selected.refresh_from_db()
        all_fields.refresh_from_db()
        self.assertTrue(selected.enabled)
        self.assertTrue(all_fields.enabled)
        self.assertEqual(get_profile_fields(selected), [retained])
        self.assertEqual(CustomField.objects.filter(pk=retained.pk).values().get(), retained_before)
        self.device.refresh_from_db()
        self.assertEqual(self.device.custom_field_data['tracer_value'], 'external value')
        retained.object_types.clear()
        selected.refresh_from_db()
        self.assertFalse(selected.enabled)
        retained.object_types.add(self.device_ct)
        self.membership(selected, retained)
        selected.refresh_from_db()
        self.assertFalse(selected.enabled)

    def test_temporarily_inactive_and_bypassed_relation_never_emit_stale_fields(self):
        field = self.field('provisioning_field')
        selected, all_fields = self.profile('selected'), self.profile('all')
        self.membership(selected, field)
        self.assertIn(field, get_profile_fields(selected))
        CustomField.objects.filter(pk=field.pk).update(status=CustomFieldStatusChoices.STATUS_PROVISIONING)
        # Queryset status writes and direct through-table writes bypass native cache invalidation.
        self.assertNotIn(field, get_profile_fields(selected))
        self.assertNotIn(field, get_profile_fields(all_fields))
        self.assertTrue(selected.profile_fields.filter(field=field).exists())
        CustomField.objects.filter(pk=field.pk).update(status=CustomFieldStatusChoices.STATUS_ACTIVE)
        CustomField.objects.clear_cache()
        self.assertIn(field, get_profile_fields(selected))
        through = CustomField.object_types.through
        through.objects.filter(customfield_id=field.pk, contenttype_id=self.device_ct.pk).delete()
        self.assertTrue(selected.profile_fields.filter(field=field).exists())
        self.assertNotIn(field, get_profile_fields(selected))
        self.assertNotIn(field, get_profile_fields(all_fields))
