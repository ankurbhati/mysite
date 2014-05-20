from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice,Poll

class IndexView( generic.ListView ) :
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll'

    def get_queryset(self):
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('pub_date')

class DetailsView( generic.DetailView ) :
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/result.html'

def vote( request, poll_id ) :
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll' : p,
            'error_message' :'You didnot select a choice',
        })
    else:
        selected_choice.votes += 1;
        selected_choice.save()
        return HttpResponseRedirect( reverse('polls:results', args=(p.id,) ) )


# Create your views here.
