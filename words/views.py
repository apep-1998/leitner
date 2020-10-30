from django.shortcuts import render
from django.shortcuts import redirect
from django import views
from datetime import datetime, timedelta
from random import shuffle, choice
import pytz
from words.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from leitner.views import get_numbers
from words.tools import get_word_means


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


@login_required
def addall(request):
    words = WordModel.objects.all()
    users = User.objects.all()
    out = 0
    for word in words:
        for user in users:
            if len(LeitnerModel.objects.filter(user_id=user.pk, word_id=word.pk)) == 0:
                LeitnerModel(word_id=word.pk, user_id=user.pk).save()
                out += 1

    return HttpResponse("{} added".format(out//len(users)))


def filter_mean_timeout_words(words):
    words = list(words)
    shuffle(words)
    for word in words:
        if(0 <= word.word_mean_level < len(levels) and
           word.word_mean_date + levels[word.word_mean_level] < datetime.now(tz=pytz.utc)):
            return word
    return None


def filter_spell_timeout_words(words):
    words = list(words)
    shuffle(words)
    for word in words:
        if(0 <= word.word_spell_level < len(levels) and
           word.word_spell_date + levels[word.word_spell_level] < datetime.now(tz=pytz.utc)):
            return word
    return None

# Create your views here.


class MeanTest(views.View):

    def get(self, request, is_true=-1):
        word = filter_mean_timeout_words(
            LeitnerModel.objects.filter(user=request.user))

        if word:
            answers = []
            random_words = list(WordModel.objects.all())
            shuffle(random_words)
            random_words = random_words[0:5]
            for w in random_words:
                if w.pk != word.word.pk:
                    ans = list(filter(lambda x: x != "", [
                               x.strip() for x in w.means.split(";")]))
                    answers.append(choice(ans))
            answers.append(choice(list(filter(lambda x: x != "", [
                           x.strip() for x in word.word.means.split(";")]))))
            shuffle(answers)
            page_data = locals()
            page_data.update(get_numbers(request))
            return render(request, "mean_test.html", page_data)
        else:
            return redirect("index")

    def post(self, request):
        pk = request.POST.get("pk")
        answer = request.POST.get("ans")
        word = LeitnerModel.objects.get(pk=pk)
        is_true = 0
        if word.user == request.user and filter_mean_timeout_words([word, ]):
            answers = list(filter(lambda x: x != "", [
                           x.strip() for x in word.word.means.split(";")]))
            if answer in answers:
                word.word_mean_level += 1
                word.word_mean_date = datetime.now(tz=pytz.utc)
                word.save()
                is_true = 1
            else:
                word.word_mean_level = 0
                word.word_mean_date = datetime.now(tz=pytz.utc)
                word.save()

        return self.get(request, is_true)


class SpellTest(views.View):

    def get(self, request, is_true=-1):
        word = filter_spell_timeout_words(
            LeitnerModel.objects.filter(user=request.user))
        if word:
            page_data = locals()
            page_data.update(get_numbers(request))
            return render(request, "spell_test.html", page_data)
        else:
            return redirect("index")

    def post(self, request):
        pk = request.POST.get("pk")
        answer = request.POST.get("ans").lower()
        word = LeitnerModel.objects.get(pk=pk)
        is_true = 0
        print(answer)
        if word.user == request.user and filter_spell_timeout_words([word, ]):
            if answer.strip() == word.word.word.strip():
                word.word_spell_level += 1
                word.word_spell_date = datetime.now(tz=pytz.utc)
                word.save()
                is_true = 1
            else:
                word.word_spell_level = 0
                word.word_spell_date = datetime.now(tz=pytz.utc)
                word.save()

        return self.get(request, is_true)


class MeanReview(views.View):
    def get(self, request, page=-1):
        words = list(filter(lambda x: x.word_mean_level < 1,
                            LeitnerModel.objects.filter(user=request.user)))
        if words:
            if page == -1:
                word = words[0]
                means = word.word.means.split(";")
                if len(words) > 1:
                    next_page = words[1]
            else:
                for i in range(len(words)):
                    if words[i].pk == page:
                        if i-1 >= 0:
                            back_page = words[i-1]
                        if i+1 < len(words):
                            next_page = words[i+1]
                        word = words[i]
                        means = word.word.means.split(";")
                        break
            page_data = locals()
            page_data.update(get_numbers(request))
            return render(request, "mean_review.html", page_data)
        else:
            return redirect("index")


class SpellReview(views.View):

    def get(self, request):
        word = list(filter(lambda x: x.word_spell_level < 1,
                           LeitnerModel.objects.filter(user=request.user)))
        if word:
            word = word[0]
            page_data = locals()
            page_data.update(get_numbers(request))
            return render(request, "spell_review.html", page_data)
        else:
            return redirect("index")

    def post(self, request):
        pk = request.POST.get("pk")
        answer = request.POST.get("ans").lower()
        word = LeitnerModel.objects.get(pk=pk)
        if word.user == request.user and word.word_spell_level < 1:
            if answer.strip() == word.word.word.strip():
                words = list(filter(lambda x: x.word_spell_level <
                                    1, LeitnerModel.objects.filter(user=request.user)))
                for word in words:
                    if word.pk > int(pk):
                        page_data = locals()
                        page_data.update(get_numbers(request))
                        return render(request, "spell_review.html", page_data)
                else:
                    return redirect("index")
            else:
                is_true = 0
                page_data = locals()
                page_data.update(get_numbers(request))
                return render(request, "spell_review.html", page_data)



class AddWord(views.View):
    
    def get(self, request):
        page_data = locals()
        page_data.update(get_numbers(request))
        return render(request, "add_word.html", page_data)

    def post(self, request):
        word = request.POST.get("word").strip().lower()
        have_mean = request.POST.get("have_mean")
        if have_mean:
            means = []
            k = 0
            while k<30:
                if request.POST.get("mean{}".format(k)):
                    means.append(request.POST.get("mean{}".format(k)).strip())
                k+=1
            if word and means:
                word_obj = WordModel(word=word, means=";".join(means))
                word_obj.save()
                for user in User.objects.all():
                    l = LeitnerModel(word=word_obj, user=user)
                    l.save()

                return self.get(request)

        if word:
            means, voice = get_word_means(word)
            means.append(word)
            page_data = locals()
            page_data.update(get_numbers(request))
            return render(request, "add_word.html", page_data)
            
