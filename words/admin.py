from django.contrib import admin
from words.models import WordModel, LeitnerModel

# Register your models here.
class WordAdmin(admin.ModelAdmin):
    pass
admin.site.register(WordModel, WordAdmin)


class LeitnerAdmin(admin.ModelAdmin):
    pass
admin.site.register(LeitnerModel, LeitnerAdmin)
