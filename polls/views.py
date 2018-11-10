from django.shortcuts import render,get_object_or_404
from .models import Question
from django.http import HttpResponseRedirect,HttpResponse
from django.http import Http404
from django.urls import reverse
from .models import Choice
def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
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
        return HttpResponseRedirect(reverse('polls:results', args=[question.id]))
def questions(request):
    return render(request, 'polls/questions.html')

def choices(request):
    question = request.POST['question']
    number = request.POST['number']
    questionlogid = Question.objects.create(question_text=question)
    context = {'question' : questionlogid.pk, 'number': list(range(int(number)))}
    return render(request, 'polls/choices.html', context)

def savechoices(request):
    number = request.POST['number']
    question = request.POST['question']
    question = Question.objects.get(pk=question)
    number = [int(i) for i in number[1:-1].split(",")]
    for x in number:
        s = request.POST['choice'+ str(x+1)]
        choicelogid = Choice.objects.create(question = question, choice_text=s)
    #return HttpResponse("Poll Added")
    return render(request, 'polls/added.html')
