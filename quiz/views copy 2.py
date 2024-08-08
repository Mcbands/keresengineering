from django.shortcuts import render
from .models import Quiz, Question, Answer, Result, QuizToken
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import Module, Course
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
# import secrets


class QuizListView(ListView):
    model =Quiz
    template_name = 'quiz/main.html'

    def get_queryset(self):
        courses = Course.objects.filter(students=self.request.user)
    
        if courses.exists():
            # If multiple courses are returned, you can choose one here
            course = courses.first()
            return Quiz.objects.filter(course=course)
        else:
            return Quiz.objects.none()



# @login_required
# def generate_quiz_token(request, pk):
#     # Retrieve the quiz object
#     quiz = get_object_or_404(Quiz, pk=pk)

#     # Generate a unique token using secrets module
#     token = secrets.token_urlsafe(16)  # Adjust the length as needed

#     # Save the token in the database
#     QuizToken.objects.create(quiz=quiz, user=request.user, token=token)

#     return JsonResponse({'token': token})






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



# @login_required
# def save_quiz_view(request, pk):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         questions = []
#         data = request.POST
#         data_ = dict(data.lists())

#         data_.pop('csrfmiddlewaretoken', None)
#         for k in data_.keys():
#             print('key:', k)
#             question = Question.objects.get(text=k)
#             questions.append(question)
#         print(questions) 

#         user =request.user
#         quiz = Quiz.objects.get(pk=pk)
        
#         score = 0
#         multiplier = 100 / quiz.number_of_questions
#         results = []
#         correct_answer = None

#         for q in questions:
#             a_selected = request.POST.get(q.text)
#             # print('selected', a_selected)
#             if a_selected != "":
#                 question_answers = Answer.objects.filter(question=q)
#                 for a in question_answers:
#                     if a_selected == a.text:
#                         if a.correct:
#                             score +=1
#                             correct_answer = a.text
#                     else:
#                         if a.correct:
#                             correct_answer =  a.text
                
#                 results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
    
#             else:
#                 results.append({str(q): "not answered"})

#         score_ = score * multiplier
#         Result.objects.create(quiz=quiz, user=user, score=score_)

#         if score_ >= quiz.score_to_pass:
#             return JsonResponse({'passed': True,'score': score_, 'results': results})
#         else:
#             return JsonResponse({"passed": False,'score': score_, 'results': results})
 

@login_required
def save_quiz_view(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken', None)
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
    
            else:
                results.append({str(q): "not answered"})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.score_to_pass:
            # Determine the next quiz after the current one
            next_quiz = Quiz.objects.filter(course=quiz.course, id__gt=pk).first()

            # Redirect to the next quiz if available, otherwise redirect to quiz list
            if next_quiz:
                return JsonResponse({'passed': True, 'score': score_, 'results': results, 'next_quiz_id': next_quiz.pk, 'next_quiz_title': next_quiz.name})
            else:
                return JsonResponse({'passed': True, 'score': score_, 'results': results, 'next_quiz_id': None, 'next_quiz_title': None})
        else:
            return JsonResponse({"passed": False, 'score': score_, 'results': results})




# @login_required
# def get_quiz_token(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)
#     user = request.user

#     # Check if the user already has a token for this quiz
#     existing_token = QuizToken.objects.filter(quiz=quiz, user=user).first()
#     if existing_token:
#         # Return the existing token if it exists
#         return JsonResponse({'token': existing_token.token})

#     # If no token exists, generate a new one
#     token = QuizToken.objects.create(quiz=quiz, user=user)

#     return JsonResponse({'token': token.token})


# def validate_quiz_token(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)
#     token_value = request.GET.get('token')

#     # Check if the token is valid for the given quiz
#     token = QuizToken.objects.filter(token=token_value, quiz=quiz).first()

#     if token:
#         # Token is valid, allow the user to access the quiz
#         return render(request, 'quiz/quiz.html', {'obj': quiz})
#     else:
#         # Token is invalid, deny access to the quiz
#         return HttpResponseForbidden("Invalid token or token expired.")
