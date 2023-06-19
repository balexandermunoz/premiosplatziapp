from django.db import models
from django.contrib import admin
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        # Mostrar question text
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    
    def was_published_recently(self):
        # Was published 1 day ago or less
        return (timezone.now() 
                >= self.pub_date 
                >= (timezone.now() - datetime.timedelta(days=1)))
    recently = property(was_published_recently)

class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE # Si borramos una pregunta se borrarán en cascada todas las questions asociadas
        )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.choice_text
    
     