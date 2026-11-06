from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from netbox.models import NetBoxModel
from extras.models import CustomField


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
