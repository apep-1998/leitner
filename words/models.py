from django.db import models
from django.contrib.auth.models import User
from .tools import get_voice
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json


class CartModel(models.Model):
    front = models.TextField(verbose_name=_('front'), null=False, blank=False)
    back = models.TextField(verbose_name=_('back'), null=False, blank=False)

    voice = models.FileField(null=True, blank=True,
                             verbose_name=_("voice"))
    image = models.FileField(verbose_name=_('image'), null=True, blank=True)

    def save(self, *args, **kwargs):
        self.voice = get_voice(self.back)
        super(CartModel, self).save(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.front, self.back)


class LeitnerBoxModel(models.Model):
    MODE_CHOICES = [
        ('M', 'Mean'),
        ('D', 'dictation')]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False, blank=False, verbose_name=_("User of Box"))

    mode = models.CharField(max_length=1, choices=MODE_CHOICES,
                            null=False, blank=False, verbose_name=_("mode"))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    descripsion = models.CharField(max_length=200, verbose_name=_("descripsion"), null=True, blank=True)

    def __str__(self):
        mode = "mean" if self.mode == "M" else "dictation"
        return "{} - {} - {}".format(self.user, self.name, mode)


class LeitnerItemModel(models.Model):
    box = models.ForeignKey(LeitnerBoxModel, on_delete=models.CASCADE,
                            null=False, blank=False, verbose_name=_("box name"))
    cart = models.ForeignKey(
        CartModel, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_("cart"))

    date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("last date question"))
    level = models.IntegerField(default=0, verbose_name=_("level"))

    def __str__(self):
        return "{} - {} - {}".format(self.box, self.cart, self.level)
