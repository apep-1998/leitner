from django.forms import ValidationError
from django import forms
from django.forms import ModelForm
from .models import CartModel
from .models import LeitnerBoxModel
from .models import LeitnerItemModel
import json


class CartForm(ModelForm):
    class Meta:
        model = CartModel
        fields = ['front', 'back', 'image', 'voice']

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop("mode", None)
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields["front"].widget.attrs["autofocus"] = ""

    def clean_front(self):
        data = self.cleaned_data["front"]
        data = data.strip()
        data = data.lower()
        return data

    def clean_back(self):
        data = self.cleaned_data["back"]
        data = data.strip()
        data = data.lower()
        return data


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
        fields = ['box', 'cart']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddItem2Box, self).__init__(*args, **kwargs)
        self.fields['box'].queryset = LeitnerBoxModel.objects.filter(
            user=self.user)

        self.fields['cart'].queryset = CartModel.objects.all()

    def clean_mode(self):
        data = self.cleaned_data["name"]

        boxes = LeitnerBoxModel.objects.filter(user=self.user)
        for box in boxes:
            if box.name == data and box.mode == self.cleaned_data["mode"]:
                raise ValidationError("this box name exist.")

        return self.cleaned_data["mode"]


class DictationForm(forms.Form):
    pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
    dictation = forms.CharField(max_length=20, widget=forms.TextInput(
        {"placeholder": "dictation", "autofocus": ''}))

    def clean_dictation(self):
        data = self.cleaned_data["dictation"]
        data = data.strip()
        data = data.lower()
        return data


class AnswerForm(forms.Form):
    pk = forms.IntegerField(required=True, widget=forms.HiddenInput())
    answers = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices", [])
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answers'].choices = [(item, item) for item in choices]
