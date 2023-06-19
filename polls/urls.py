from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # Ex: /polls/ -> Vista principal
    path("", views.IndexView.as_view(), name="index"),
    # Ex: /polls/5/ -> detalles de question
    path("<int:pk>/detail/", views.DetailView.as_view(), name="detail"),
    # Ex: /polls/5/results -> resultados
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
    # Ex: /polls/5/vote -> votos
    path("<int:question_id>/vote/", views.vote , name="vote"),
    
]