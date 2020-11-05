from django.forms import ValidationError
from django import forms
from django.forms import ModelForm
from .models import WordModel
from .models import LeitnerBoxModel
from .models import LeitnerItemModel
import json


class WordForm(ModelForm):
    class Meta:
        model = WordModel
        fields = ['word', 'means']

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop("mode", None)
        super(WordForm, self).__init__(*args, **kwargs)
        if self.mode == "S":
            self.fields.pop("means")
        self.fields["word"].widget.attrs["autofocus"] = ""

    def clean_word(self):
        data = self.cleaned_data["word"]
        data = data.strip()
        data = data.lower()
        return data

    def clean_means(self):
        if self.mode == "S":
            return "[]"

        data = self.cleaned_data["means"]

        data = data.split("\r\n")
        out = []
        for d in data:
            if d.strip() != "":
                out.append(d.strip())

        if len(out) == 0 and self.mode == "M":
            raise ValidationError("len means = 0")

        return json.dumps(data)


class NewBoxForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewBoxForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeitnerBoxModel
        fields = ['name', 'mode', 'descripsion']

    def clean_name(self):
        data = self.cleaned_data["name"]
        data = data.strip()
        data = data.lower()
        return data

    def clean_mode(self):
        data = self.cleaned_data["name"]
        boxes = LeitnerBoxModel.objects.filter(user=self.user)
        for box in boxes:
            if box.name == data and box.mode == self.cleaned_data["mode"]:
                raise ValidationError("this box name exist.")

        return self.cleaned_data["mode"]


class AddItem2Box(ModelForm):
    class Meta:
        model = LeitnerItemModel
        fields = ['box', 'word']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddItem2Box, self).__init__(*args, **kwargs)
        self.fields['box'].queryset = LeitnerBoxModel.objects.filter(
            user=self.user)

        # words = []
        # for word in WordModel.objects.all():
        #     user_words = LeitnerItemModel.objects.filter(word=word)
        #     for user_word in user_words:
        #         if user_word.box.user == self.user:
        #             break
        #     else:
        #         words.append(word.pk)

        # self.fields['word'].queryset = WordModel.objects.filter(pk__in=words)
        self.fields['word'].queryset = WordModel.objects.all()

    def clean_mode(self):
        data = self.cleaned_data["name"]

        boxes = LeitnerBoxModel.objects.filter(user=self.user)
        for box in boxes:
            if box.name == data and box.mode == self.cleaned_data["mode"]:
                raise ValidationError("this box name exist.")

        return self.cleaned_data["mode"]


class SpellForm(forms.Form):
    pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
    spell = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        {"placeholder": "spell", "autofocus": ''}))

    def clean_spell(self):
        data = self.cleaned_data["spell"]
        data = data.strip()
        data = data.lower()
        return data


class MeanForm(forms.Form):
    pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
    means = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices", [])
        super(MeanForm, self).__init__(*args, **kwargs)
        self.fields['means'].choices = [(item, item) for item in choices]
