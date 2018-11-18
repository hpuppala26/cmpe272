from django.shortcuts import render,get_object_or_404
from .models import Question,Choice,Voter
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request,'polls/index.html',context)
# Create your views here.
def detail(request,question_id):
    if Voter.objects.filter(question_id=question_id,user=request.user.username).exists():
        return render(request,'polls/alreadyvoted.html')
    else:
        question = get_object_or_404(Question,pk=question_id)
        return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})
def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    if Voter.objects.filter(question_id=question_id,user=request.user.username).exists():
        #return HttpResponse("YOU ALREADY VOTED")
        return render(request,'polls/alreadyvoted.html')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You Didnt select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Voter.objects.create(question_id=question_id,user=request.user.username)
        return HttpResponseRedirect(reverse('polls:results',args=[question.id]))

def questions(request):
    return render(request,'polls/questions.html')
def choices(request):
    question = request.POST['question']
    number = request.POST['number']
    questionlogid = Question.objects.create(question_text=question)
    context = {'question': questionlogid.pk , 'number':list(range(int(number)))}
    return render(request,'polls/choices.html',context)
def savechoices(request):
    number = request.POST['number']
    question = request.POST['question']
    questions = Question.objects.get(pk=question)
    number = [int(i) for i in number[1:-1].split(",")]
    for x in number:
        s = request.POST['choice'+str(x+1)]
        choicelogid = Choice.objects.create(question = questions,choice_text=s)
    return render(request,'polls/added.html',{"questionid":questions.pk})