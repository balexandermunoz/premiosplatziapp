from django.contrib import admin
from .models import Question,Choice
from django import forms
from django.forms.models import BaseInlineFormSet


class ChoiceInLine(admin.StackedInline): #StackedInline or TabularInline
    model = Choice
    extra = 3
    exclude= ['votes']

# Personalizar como se ve el modelo Question en el administrador 
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fields = ["pub_date", "question_text"] #Change order in admin
    inlines = [ChoiceInLine]
    list_display = ("question_text", "pub_date", "was_published_recently") #Display in list admin
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    
admin.site.register(Question, QuestionAdmin)