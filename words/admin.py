from django.contrib import admin
from words.models import WordModel, LeitnerBoxModel, LeitnerItemModel

@admin.register(WordModel)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "means")

@admin.register(LeitnerBoxModel)
class LeitnerBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "mode", "user", "descripsion")

@admin.register(LeitnerItemModel)
class LeitnerItemAdmin(admin.ModelAdmin):
    list_display = ("box", "word", "level", "date")
