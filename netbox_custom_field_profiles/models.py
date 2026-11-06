from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from netbox.models import NetBoxModel
from extras.models import CustomField
from django.core.exceptions import ValidationError


class CustomTabConfig(NetBoxModel):
    content_type = models.OneToOneField(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name='custom_tab_config',
    )
    tab_label = models.CharField(max_length=100, default='Parameters')
    enabled = models.BooleanField(default=True)
    fields = models.ManyToManyField(
        to=CustomField,
        through='CustomTabConfigField',
        blank=True,
        related_name='custom_tab_configs',
    )

    class Meta:
        ordering = ['content_type__app_label', 'content_type__model']
        verbose_name = 'Custom Tab Config'
        verbose_name_plural = 'Custom Tab Configs'

    def __str__(self):
        return f'{self.content_type} — {self.tab_label}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_custom_field_profiles:customtabconfig', args=[self.pk])


class CustomTabConfigGroup(models.Model):
    tab_config = models.ForeignKey(
        to=CustomTabConfig,
        on_delete=models.CASCADE,
        related_name='config_groups',
    )
    group_name = models.CharField(max_length=50)
    weight = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['weight', 'group_name']
        unique_together = [('tab_config', 'group_name')]

    def __str__(self):
        return f'{self.tab_config} / {self.group_name} (weight={self.weight})'


class CustomTabConfigField(models.Model):
    tab_config = models.ForeignKey(
        to=CustomTabConfig,
        on_delete=models.CASCADE,
        related_name='config_fields',
    )
    field = models.ForeignKey(
        to=CustomField,
        on_delete=models.CASCADE,
        related_name='+',
    )
    weight = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['weight', 'field__name']
        unique_together = [('tab_config', 'field')]

    def __str__(self):
        return f'{self.tab_config} / {self.field.name} (weight={self.weight})'


class CustomFieldProfile(NetBoxModel):
    """Presentation configuration referencing native Device custom fields."""

    FIELD_MODE_SELECTED = 'selected'
    FIELD_MODE_ALL = 'all'
    FIELD_MODES = ((FIELD_MODE_SELECTED, 'Selected fields'), (FIELD_MODE_ALL, 'All applicable fields'))

    title = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=100)
    enabled = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='custom_field_profiles')
    field_mode = models.CharField(max_length=16, choices=FIELD_MODES, default=FIELD_MODE_SELECTED)
    fields = models.ManyToManyField(CustomField, through='ProfileField', blank=True, related_name='field_profiles')
    device_types = models.ManyToManyField('dcim.DeviceType', blank=True, related_name='custom_field_profiles')
    device_roles = models.ManyToManyField('dcim.DeviceRole', blank=True, related_name='custom_field_profiles')
    applicability_tags = models.ManyToManyField('extras.Tag', blank=True, related_name='applicable_field_profiles')

    class Meta:
        ordering = ['display_order', 'title', 'created', 'pk']

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.content_type_id and (self.content_type.app_label, self.content_type.model) != ('dcim', 'device'):
            raise ValidationError({'content_type': 'Profiles currently support Devices only.'})

    def get_absolute_url(self):
        return reverse('plugins:netbox_custom_field_profiles:customfieldprofile', args=[self.pk])


class ProfileField(models.Model):
    profile = models.ForeignKey(CustomFieldProfile, on_delete=models.CASCADE, related_name='profile_fields')
    field = models.ForeignKey(CustomField, on_delete=models.CASCADE, related_name='+')
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'pk']
        constraints = [models.UniqueConstraint(fields=['profile', 'field'], name='unique_profile_field')]

    def __str__(self):
        return f'{self.profile} / {self.field.name}'
