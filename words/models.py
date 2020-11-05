from django.db import models
from django.contrib.auth.models import User
from words.tools import get_voice_name
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json


class WordModel(models.Model):
    word = models.CharField(max_length=20, null=False,
                            blank=False, verbose_name=_("word"))
    means = models.TextField(verbose_name=_("means"))
    voice = models.FileField(null=True, blank=True,
                             verbose_name=_("word voice"))

    def get_means(self):
        if self.means == "":
            return []
        return json.loads(self.means)

    def save(self, *args, **kwargs):
        self.voice = get_voice_name(self.word)
        super(WordModel, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.word)


class LeitnerBoxModel(models.Model):
    MODE_CHOICES = [
        ('M', 'Mean'),
        ('S', 'Spell')]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False, blank=False, verbose_name=_("User of Box"))

    mode = models.CharField(max_length=1, choices=MODE_CHOICES,
                            null=False, blank=False, verbose_name=_("mode"))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    descripsion = models.CharField(max_length=200, verbose_name=_("descripsion"))

    def __str__(self):
        mode = "mean" if self.mode == "M" else "spell"
        return "{} - {} - {}".format(self.user, self.name, mode)


class LeitnerItemModel(models.Model):
    box = models.ForeignKey(LeitnerBoxModel, on_delete=models.CASCADE,
                            null=False, blank=False, verbose_name=_("box name"))
    word = models.ForeignKey(
        WordModel, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_("word"))

    date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("last date question"))
    level = models.IntegerField(default=0, verbose_name=_("level"))

    def __str__(self):
        return "{} - {} - {}".format(self.box, self.word, self.level)
