from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import SuggestionForm

from .models import Choice, Question, Suggestion

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class SuggestionsView(generic.ListView):
    model = Suggestion
    template_name = 'polls/suggestions.html'
#    fields = ('name','text')
#    def get(self, request):
#        form = SuggestionForm()
#        return render(request, 'polls/suggestions.html', {'form' : form})
    def post(self, request):
#        form = SuggestionForm(request.POST)
#        if form.is_valid():
#            form.save()
#            name = form.cleaned_data['name']
#            text = form.cleaned_data['text']
#            form = SuggestionForm()
        name = request.POST['name']
        text = request.POST['text']
        new_suggestion = Suggestion(name=name, text=text)
        new_suggestion.save()
        args = {'name':name, 'text':text}
        return render(request, 'polls/suggestions.html', args)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def suggestion_list(request):
    all_suggestions = Suggestion.objects.all()
    #context_object_name = 'all_suggestions'
    context = {'all_suggestions' : all_suggestions}
    return render(request, 'polls/suggestions_list.html', context)

#class SuggestionsListView(generic.ListView):
    #model = SuggestionList
    #template_name = 'polls/suggestions/list.html'
    #def get_queryset(self):
    #    return Suggestion.objects