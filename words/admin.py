from django.contrib import admin
from words.models import WordModel, LeitnerBoxModel, CategoryModel, LeitnerItemModel

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "descripsion")

@admin.register(WordModel)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "means", "categorys")

@admin.register(LeitnerBoxModel)
class LeitnerBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "mode", "user", "descripsion")

@admin.register(LeitnerItemModel)
class LeitnerItemAdmin(admin.ModelAdmin):
    list_display = ("box", "word", "level", "date")
