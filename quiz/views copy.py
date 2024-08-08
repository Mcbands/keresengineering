from django.shortcuts import render
from .models import Quiz, Question, Answer, Result
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import Module, Course
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


class QuizListView(ListView):
    model =Quiz
    template_name = 'quiz/main.html'

    # def get_queryset(self):
    #     course = get_object_or_404(Course, students=self.request.user)
    #     return Quiz.objects.filter(course=course)

    def get_queryset(self):
        courses = Course.objects.filter(students=self.request.user)
    
        if courses.exists():
            # If multiple courses are returned, you can choose one here
            course = courses.first()
            return Quiz.objects.filter(course=course)
        else:
            return Quiz.objects.none()



@login_required
def quiz_view(request, pk):
    # Retrieve the quiz object
    quiz = get_object_or_404(Quiz, pk=pk)
    
    try:
        # Check if the user is enrolled in the course associated with the quiz
        if not request.user.main_enrolled_courses.filter(pk=quiz.course.pk).exists():
            return HttpResponseForbidden("You are not enrolled in this course.")
    except Course.DoesNotExist:
        return HttpResponseForbidden("This quiz is associated with a course that doesn't exist.")

    # If the user is enrolled, render the quiz template
    return render(request, 'quiz/quiz.html', {'obj': quiz})


@login_required
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


@login_required
def save_quiz_view(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken', None)
        for k in data_.keys():
            print('key:', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions) 

        user =request.user
        quiz = Quiz.objects.get(pk=pk)
        
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            # print('selected', a_selected)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer =  a.text
                
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
    
            else:
                results.append({str(q): "not answered"})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.score_to_pass:
            return JsonResponse({'passed': True,'score': score_, 'results': results})
        else:
            return JsonResponse({"passed": False,'score': score_, 'results': results})
 

