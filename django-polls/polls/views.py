from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, get_object_or_404

# Typing
from typing import Any
from django.core.handlers.wsgi import WSGIRequest
from django.core.handlers.asgi import ASGIRequest
from django.db.models import QuerySet

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lt=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.filter(pub_date__lt=timezone.now())


# def index(request: WSGIRequest | ASGIRequest) -> HttpResponse:
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     return render(
#         request, "polls/index.html", {"latest_question_list": latest_question_list}
#     )


# def detail(request: WSGIRequest | ASGIRequest, question_id: str) -> HttpResponse:
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request: WSGIRequest | ASGIRequest, question_id: str) -> HttpResponse:
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {
#         "question": question
#     })


def vote(request: WSGIRequest | ASGIRequest, question_id: str) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(ok=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice"},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
