from django import views
from random import shuffle, choice
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from .forms import WordForm
from .forms import NewBoxForm
from .forms import AddItem2Box
from .forms import SpellForm
from .forms import MeanForm

from .models import LeitnerBoxModel
from .models import LeitnerItemModel
from .models import WordModel
import pytz

from .tools import get_word_means

levels = [
    timedelta(minutes=1),
    timedelta(hours=20),
    timedelta(days=1, hours=20),
    timedelta(days=3, hours=20),
    timedelta(days=7, hours=20),
    timedelta(days=14, hours=20)]


def index_view(request):
    all_user_words = 0
    all_user_boxes = 0
    all_in_box_words = 0
    ready_to_question = 0
    boxes = LeitnerBoxModel.objects.filter(user=request.user)
    ready_word_number = []
    ready_review = []
    for box in boxes:
        all_user_words += LeitnerItemModel.objects.filter(box=box).count()
        all_user_boxes += 1
        all_in_box_words += LeitnerItemModel.objects.filter(box=box, level__lt=6).count()
        ready_word_number.append(len(get_box_ready_words(box)))
        ready_review.append(LeitnerItemModel.objects.filter(box=box, level=0).count())
    ready_to_question = sum(ready_word_number)
    boxes = zip(boxes, ready_word_number, ready_review)        
    return render(request, "home.html", locals())

def get_box_ready_words(box):
    out = []
    words = LeitnerItemModel.objects.filter(box=box)
    for word in words:
        if(0 <= word.level < len(levels) and 
           word.date + levels[word.level] < datetime.now(tz=pytz.utc)):
            out.append(word)
    
    return out

@login_required
def remove_box(request, box_pk):
    LeitnerBoxModel.objects.get(pk=box_pk).delete()
    return redirect("box_list")

@login_required
def copy_box(request, box_pk):
    box = LeitnerBoxModel.objects.get(pk=box_pk)
    user = request.user
    if box.user != user:
        boxes = LeitnerBoxModel.objects.get(user=user)
        for b in boxes:
            if b.name == box.name and b.mode == box.mode:
                break
        else:
            leitner_items = LeitnerItemModel.objects.filter(box=box)
            box.pk = None
            box.user = user
            box.save()
            for item in leitner_items:
                item.pk = None
                item.box = box
                item.level = 0
                item.date = datetime.now(tz=pytz.utc)
                item.save()
                
    return redirect("box_list")


def get_means(request, word):
    means, voice = get_word_means(word)
    out = {
        "means" : "\r\n".join(means[0:5]),
    }
    print(out)
    return JsonResponse(out)

class AddBox(views.View):
    title = "اضافه جعبه لایتنر"
    tips = []
    def get(self, request, success=False):
        form = NewBoxForm()
        return render(request, "form.html", locals())
    
    def post(self, request):
        form = NewBoxForm(request.POST, user=request.user)
        if form.is_valid():
            LeitnerBoxModel(user=request.user,
                mode=form.cleaned_data["mode"],
                name=form.cleaned_data["name"],
                descripsion=form.cleaned_data["descripsion"]).save()
            return self.get(request, True)
        return render(request, "form.html", locals())


class Add2Box(views.View):
    title = "اضافه کردن کلمه به جعبه"
    tips = [
        "برای اضافه کردن چند معنی به جمله هر معنی را در یک خط بنویسید."
    ]
    def get(self, request, box_pk, success=False):
        box = LeitnerBoxModel.objects.get(pk=box_pk)
        if box.user == request.user:
            form = WordForm(mode=box.mode)
            return render(request, "form.html", locals())

        return redirect("index")
    
    def post(self, request, box_pk):
        box = LeitnerBoxModel.objects.get(pk=box_pk)
        ## check box for user
        if box.user == request.user:
    
            form = WordForm(request.POST, mode=box.mode)

            if form.is_valid():
                word = form.save()
                LeitnerItemModel(box=box, word=word).save()
                return self.get(request, box_pk=box_pk, success=True)

            return render(request, "form.html", locals())

        return redirect("index")

class BoxList(ListView):
    template_name = "box_list.html"
    model = LeitnerBoxModel
    paginate_by = 20  # if pagination is desired
    
    def get_queryset(self):
        queryset = super(BoxList, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset



class MeanBoxList(views.View):
    title = "جعبه های معنی"
    tips = []
    heads = ["نام", "تعداد کل کلمات", "تعداد کلمات آماده آزمون", "کلمات قابل مرور" , "توضیحات", "فعالیت ها"]
    def get(self, request):
        items = []
        for box in LeitnerBoxModel.objects.filter(user=request.user, mode="M"):
            item = [box.name,]
            item.append(LeitnerItemModel.objects.filter(box=box).count())
            item.append(len(get_box_ready_words(box)))
            item.append(LeitnerItemModel.objects.filter(box=box, level=0).count())
            item.append(box.descripsion)
            items.append((box.pk, item))

        return render(request, "list.html", locals())
    
    def post(self, request):
        pass


class SpellBoxList(views.View):
    title = "جعبه های املا"
    tips = []
    heads = ["نام", "تعداد کل کلمات", "تعداد کلمات آماده آزمون", "کلمات قابل مرور" , "توضیحات", "فعالیت ها"]
    def get(self, request):
        items = []
        for box in LeitnerBoxModel.objects.filter(user=request.user, mode="S"):
            item = [box.name,]
            item.append(LeitnerItemModel.objects.filter(box=box).count())
            item.append(len(get_box_ready_words(box)))
            item.append(LeitnerItemModel.objects.filter(box=box, level=0).count())
            item.append(box.descripsion)
            items.append((box.pk, item))

        return render(request, "list.html", locals())
    
    def post(self, request):
        pass


def get_random_answers(word):
    means = []
    for w in WordModel.objects.filter(~Q(pk = word.pk)):
        try:
            means.append(choice(w.get_means()))
        except:
            pass
    shuffle(means)
    means = means[0:3]
    means.append(choice(word.get_means()))
    shuffle(means)
    means.append("I don't know!")
    return means

def level_up_item(word, box):
    box_item = LeitnerItemModel.objects.get(box=box, word=word)
    box_item.level += 1
    box_item.date = datetime.now(tz=pytz.utc)
    box_item.save()
    
def restart_item(word, box):
    box_item = LeitnerItemModel.objects.get(box=box, word=word)
    box_item.level = 0
    box_item.date = datetime.now(tz=pytz.utc)
    box_item.save()
    

class TestBox(views.View):

    def get(self, request, box_pk, last_answer=None):
        box = LeitnerBoxModel.objects.get(pk=box_pk)
        if box.user == request.user:
            try:
                word = choice(get_box_ready_words(box)).word
                print(word)
            except:
                return redirect("index")
                
            if box.mode == "M":
                means = get_random_answers(word)
                form = MeanForm(choices=means, initial={"pk": word.pk})
            else:
                form = SpellForm(initial={"pk": word.pk})
            return render(request, "test.html", locals())

        return redirect("index")

    def post(self, request, box_pk):
        box = LeitnerBoxModel.objects.get(pk=box_pk)
        if box.user == request.user:
            last_answer = None
            if box.mode == "M":
                form = MeanForm(request.POST)
                form.is_valid()
                word = WordModel.objects.get(pk=form.cleaned_data["pk"])
                means = word.get_means()
                form = MeanForm(request.POST, choices=means)
                if word.word in [w.word.word for w in get_box_ready_words(box)]:
                    if form.is_valid():
                        last_answer = True
                        level_up_item(word, box)
                    else:
                        last_answer = False
                        restart_item(word, box)
            else:
                form = SpellForm(request.POST)
                if form.is_valid():
                    word = WordModel.objects.get(pk=form.cleaned_data["pk"])
                    if word.word in [w.word.word for w in get_box_ready_words(box)]:
                        if word.word == form.cleaned_data["spell"]:
                            last_answer = True
                            level_up_item(word, box)
                        else:
                            last_answer = False
                            restart_item(word, box)
                else:
                    print(form.errors)
                
            return self.get(request, box_pk, last_answer)
        else:
            return redirect("index")

class ReviewBox(views.View):
    title = "مرور کلمات جعبه"
    def get(self, request, box_pk, last_answer=None):
        box = LeitnerBoxModel.objects.get(pk=box_pk)
        if box.user == request.user:
            words = [(item.word.word, ",".join(item.word.get_means()), item.word.voice) for item in LeitnerItemModel.objects.filter(box=box, level=0)]
            print(words)
            return render(request, "review_list.html", locals())
        
        return redirect("index")
            
