from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Item Name'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')