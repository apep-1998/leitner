from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta
import pytz
from words.models import *
from django.contrib.auth.models import User


levels = [
    timedelta(minutes=1),
    timedelta(hours=20),
    timedelta(days=1, hours=20),
    timedelta(days=3, hours=20),
    timedelta(days=7, hours=20),
    timedelta(days=14, hours=20),
    timedelta(days=29, hours=20),
    timedelta(days=59, hours=20),
    timedelta(days=119, hours=20),
]

def filter_mean_timeout_words(words):
    out = []
    for word in words:
        if(0 <= word.word_mean_level < len(levels) and 
           word.word_mean_date + levels[word.word_mean_level] < datetime.now(tz=pytz.utc)):
                out.append(word)
    return out

def filter_spell_timeout_words(words):
    out = []
    for word in words:
        if(0 <= word.word_spell_level < len(levels) and 
           word.word_spell_date + levels[word.word_spell_level] < datetime.now(tz=pytz.utc)):
                out.append(word)
    return out

def get_numbers(request):
    new_spell_word = len(filter_spell_timeout_words(LeitnerModel.objects.filter(user=request.user)))
    spell_review = len(list(filter(lambda x: x.word_spell_level < 1, LeitnerModel.objects.filter(user=request.user))))
    new_mean_word = len(filter_mean_timeout_words(LeitnerModel.objects.filter(user=request.user)))
    mean_review = len(list(filter(lambda x: x.word_mean_level < 1, LeitnerModel.objects.filter(user=request.user))))
    return locals()

@login_required
def index(request):
    # score_list = []
    # for user in User.objects.all():
    #     score = 0
    #     for word in LeitnerModel.objects.filter(user=user):
    #         score += word.word_spell_level * 2
    #         score += word.word_mean_level
    #     score_list.append({"user": user, "score":score})
    # score_list.sort(reverse=True, key=lambda x: x['score'])
    # page_data = locals()
    # page_data.update(get_numbers(request))
    return render(request, "home.html", locals())

