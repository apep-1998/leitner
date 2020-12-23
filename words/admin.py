from django.contrib import admin
from words.models import CartModel, LeitnerBoxModel, LeitnerItemModel

@admin.register(CartModel)
class WordAdmin(admin.ModelAdmin):
    list_display = ("front", "back")

@admin.register(LeitnerBoxModel)
class LeitnerBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "mode", "user", "descripsion")

@admin.register(LeitnerItemModel)
class LeitnerItemAdmin(admin.ModelAdmin):
    list_display = ("box", "cart", "level", "date")
