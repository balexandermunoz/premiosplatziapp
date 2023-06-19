from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Return the last five published questions"""
        # order_by Like filter but ordered. The miunus is Desc (De las más nuevas a las más viejas)
        return (
            Question.objects.filter(pub_date__lte=timezone.now()) #lte: less than equal now
            .order_by("-pub_date")[:5]
            )

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """Exludes any questions that are not published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())
        
class ResultView(DetailView):
    template_name = "polls/results.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())  

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Id de la choice en detail form: (Name="choice")
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Reverse es para no hard codear el vínculo (como la etiqueta url): 
        # polls:results = path en urls <int:question_id>/results/
        # Y si es un form usar Redirect para evitar ataques
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))