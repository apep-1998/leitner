from django.db import models
from django.contrib.auth.models import User
from words.tools import get_voice_name


# Create your models here.
class WordModel(models.Model):
    word = models.CharField(unique=True, max_length=20, null=False, blank=False, verbose_name="work key")
    means = models.TextField(null=False, blank=False, verbose_name="means")
    voice = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.voice = get_voice_name(self.word)
        super(WordModel, self).save(*args, **kwargs)
        
    def __str__(self):
        return "{}".format(self.word)

class LeitnerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name="user of this word")
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE, null=False, blank=False, verbose_name="word")
    word_mean_date = models.DateTimeField(auto_now_add=True, verbose_name="last date question for mean")
    word_mean_level = models.IntegerField(default=0, verbose_name="mean level")
    word_spell_date = models.DateTimeField(auto_now_add=True, verbose_name="last date question for spell")
    word_spell_level = models.IntegerField(default=0, verbose_name="spell level")
    
    def __str__(self):
        return "{} - {}".format(self.user, self.word)
    
