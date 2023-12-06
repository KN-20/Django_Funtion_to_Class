from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Choice, Question
from django.views.generic import ListView, DetailView


# Create your views here.
class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class ResultView(DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_object(self, queryset=None):
        object = get_object_or_404(Question, id=self.kwargs['question_id'])
        return object


class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None):
        object = get_object_or_404(Question, id=self.kwargs['question_id'])
        return object

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_massage': "you didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
