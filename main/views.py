# Standard Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# from quiz.models import Question
from django.http import HttpResponse
import pytz
from .forms import CourseEditForm
from .models import Course, Enrollment, Module
from django.db.models import Prefetch
from quiz.models import Quiz
# from quiz.models import Question, Mark
from django.http import JsonResponse
# from quiz.models import Question, Mark
from django.urls import reverse
from django.http import HttpResponse


def category_detail(request, category_slug):
    # Retrieve courses based on category_slug
    courses = Course.objects.filter(category__slug=category_slug)
    # Add any additional context data needed for the template
    context = {
        'courses': courses,
        'category_slug': category_slug,
    }
    return render(request, 'category_detail.html', context)

def level_detail(request, level_slug):
    # Retrieve courses based on level_slug
    courses = Course.objects.filter(level__slug=level_slug)
    # Add any additional context data needed for the template
    context = {
        'courses': courses,
        'level_slug': level_slug,
    }
    return render(request, 'level_detail.html', context)




def redirect_dash(request, course_id):
    return redirect(reverse('dash'))

def redirect_dash_no_id(request):
    return redirect(reverse('dash'))



@login_required
def module_detail(request, module_id):
    modules = Module.objects.all()
    module = get_object_or_404(Module, id=module_id)
    main = Module.objects.all()


    module_index = list(modules).index(module)

    # Calculate the index of the previous and next modules
    prev_module_index = module_index - 1 if module_index > 0 else None
    next_module_index = module_index + 1 if module_index < len(modules) - 1 else None

    context = {
        'modules': modules,
        'module': module,
        'main_module': main,
        'prev_module_id': modules[prev_module_index].id if prev_module_index is not None else None,
        'next_module_id': modules[next_module_index].id if next_module_index is not None else None,
    }
    return render(request, 'school/module_detail.html', context)


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course_modules = Module.objects.filter(course=module.course).order_by('id')

    module_index = list(course_modules).index(module)

    # Calculate the index of the previous and next modules within the same course
    prev_module_index = module_index - 1 if module_index > 0 else None
    next_module_index = module_index + 1 if module_index < len(course_modules) - 1 else None

    context = {
        'module': module,
        'prev_module_id': course_modules[prev_module_index].id if prev_module_index is not None else None,
        'next_module_id': course_modules[next_module_index].id if next_module_index is not None else None,
    }
    return render(request, 'school/module_detail.html', context)









def pay(request):
    return render(request, 'pay.html')



def about(request):
    return render(request, 'school/about.html')

def error_404(request, exception):
    return render(request, 'error404.html', {})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'school/courses.html', {'courses': courses})



def dashboard_home(request):
    modules = Module.objects.all()
    user = request.user
    courses_uploaded = Course.objects.filter(instructor=user)
    num_courses_uploaded = courses_uploaded.count()
    courses_enrolled = Course.objects.filter(students=user)
    num_courses_enrolled = courses_enrolled.count()
    num_students = Enrollment.objects.filter(course__in=courses_uploaded).values('student').distinct().count()
    
    instructor = request.user
    courses = Course.objects.filter(instructor=instructor)

    enrollments = []
    ist_tz = pytz.timezone('Asia/Kolkata')

    for course in courses:
        course_enrollments = Enrollment.objects.filter(course=course)
        for enrollment in course_enrollments:
            student = enrollment.student
            enrollment_date_ist = enrollment.enrolled_at.astimezone(ist_tz)
            enrollment_date = enrollment_date_ist.strftime('%d %B %Y %H:%M:%S')
            enrollments.append({'course_title': course.title, 'student_name': student.username, 'enrollment_date': enrollment_date})

    context = {
        'courses_uploaded': courses_uploaded,
        'num_courses_uploaded': num_courses_uploaded,
        'num_courses_enrolled': num_courses_enrolled,
        'num_students': num_students,
        'enrollments': enrollments,
        'modules': modules ,
    }
    return render(request, 'dashboard/home.html', context)


def profile(request):
    user = request.user
    email = user.email
    full_name = f"{user.first_name} {user.last_name}"
    username = user.username
    return render(request, 'dashboard/profile.html', {'email': email, 'full_name': full_name, 'username': username})


def courses_enrolled(request):
    user = request.user
    courses = Course.objects.filter(students=user)
    context = {
        'courses': courses
    }
    return render(request, 'dashboard/courses-enrolled.html', context)


def courses_uploaded(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'dashboard/courses-uploaded.html', {'courses': courses})

@login_required
def upload(request):
    if request.method == 'POST':
        # Get course details from the form
        title = request.POST['title']
        description = request.POST['description']
        thumbnail = request.FILES['thumbnail']
        featured_video = request.FILES['featured_video']
        instructor = request.user
        duration = request.POST['duration']
        level = request.POST['level']
        requirements = request.POST['requirements']
        content = request.POST['content']
        category = request.POST['category']
        price = int(request.POST['price'])
        discount = int(request.POST['discount'])

        lesson_title = request.POST['lesson_title']
        lesson_video = request.FILES['lesson_video']

        discounted_price = (discount/100)*price
        price = price-discounted_price

        # Split requirements and content into lists
        requirements_list = [r.strip() for r in requirements.split(', ')]
        content_list = [c.strip() for c in content.split(', ')]

        # Upload thumbnail and featured video to Cloudinary
        thumbnail_upload = cloudinary.uploader.upload(thumbnail)
        featured_video_upload = cloudinary.uploader.upload(
            featured_video, resource_type="video")

        # Upload lesson videos to Cloudinary
        lesson_video_upload = cloudinary.uploader.upload(
            lesson_video, resource_type="video")

        # Create a new Course object with the given details
        course = Course(
            title=title,
            description=description,
            thumbnail=thumbnail_upload['secure_url'],
            featured_video=featured_video_upload['secure_url'],
            instructor=instructor,
            duration=duration,
            level=level,
            requirements=requirements_list,
            content=content_list,
            category=category,
            price=price,
            discount=discount,
            lesson_title=lesson_title,
            lesson_video=lesson_video_upload['secure_url'],
            )
        course.save()

    return render(request, 'dashboard/upload.html')


def course_details(request, instructor, slug):
    instructor_obj = get_object_or_404(User, username=instructor)
    course = get_object_or_404(Course, slug=slug, instructor=instructor_obj)
    category_courses = Course.objects.filter(category__iexact=course.category).exclude(id=course.id)[:3]

    enrolled = False
    
    if request.user.is_authenticated:
        enrolled = course.students.filter(id=request.user.id).exists()

    if request.method == 'POST' and not enrolled:
        user = request.user
        course.students.add(user)
        enrollment = Enrollment(student=user, course=course)
        enrollment.save()
        messages.success(request, 'You have enrolled in this course!')
        return redirect('course_details', instructor=instructor, slug=slug)

    context = {
        'course': course,
        'enrolled': enrolled,
        'category_courses': category_courses,
        'instructor': instructor
    }
    return render(request, 'school/course.html', context)

@login_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        form = CourseEditForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
    else:
        form = CourseEditForm(instance=course)
    return render(request, 'dashboard/course-edit.html', {'form': form, 'course': course})

@login_required
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('/dashboard/courses-uploaded')
    context = {
        'course': course,
    }
    return render(request, 'dashboard/course-edit.html', context)

def category(request, category):
    courses = Course.objects.filter(category__iexact=category)
    context = {
        'category': category,
        'courses': courses
    }
    return render(request, 'school/category.html', context)


@login_required
def dash(request, course_id=None):
    if course_id is not None:
        course = Course.objects.get(pk=course_id)
        main = Module.objects.all()
        # modules = course.module_set.all()
        modules = course.course_modules.all()


        user = request.user
        courses_uploaded = Course.objects.filter(instructor=user)
        num_courses_uploaded = courses_uploaded.count()
        courses_enrolled = Course.objects.filter(students=user)
        num_courses_enrolled = courses_enrolled.count()
        num_students = Enrollment.objects.filter(course__in=courses_uploaded).values('student').distinct().count()
    
        instructor = request.user
        courses = Course.objects.filter(instructor=instructor)

        enrollments = []
        ist_tz = pytz.timezone('Asia/Kolkata')

        for course in courses:
            course_enrollments = Enrollment.objects.filter(course=course)
            for enrollment in course_enrollments:
                student = enrollment.student
                enrollment_date_ist = enrollment.enrolled_at.astimezone(ist_tz)
                enrollment_date = enrollment_date_ist.strftime('%d %B %Y %H:%M:%S')
                enrollments.append({'course_title': course.title, 'student_name': student.username, 'enrollment_date': enrollment_date})

        context = {
            'modules': modules,
            'course': course,
            'main':main,
            'courses_uploaded': courses_uploaded,
        'num_courses_uploaded': num_courses_uploaded,
        'num_courses_enrolled': num_courses_enrolled,
        'num_students': num_students,
        'enrollments': enrollments,
        }
        return render(request, 'school/dash.html', context)
    else:
        # Handle case when course_id is not provided
        return HttpResponse("No course ID provided.")








   
def quiz_details(request, course_id, quiz_id):
    course = get_object_or_404(Course, pk=course_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    return render(request, 'school/quiz_details.html', {'course': course, 'quiz': quiz})




def bases(request):
    modules = Module.objects.all()
    quiz = get_object_or_404(Question, id=quiz_id)
    course = Course.objects.all()
    quizzes = Question.objects.all()
    mark = Mark.objects.all()
    quiz_index = list(quizzes).index(quiz)

    prev_quiz_index = quiz_index - 1 if quiz_index > 0 else None
    next_quiz_index = quiz_index + 1 if quiz_index < len(quizzes) - 1 else None

    context = {
        
        'prev_quiz_id': quizzes[prev_quiz_index].id if prev_quiz_index is not None else None,
        'next_quiz_id': quizzes[next_quiz_index].id if next_quiz_index is not None else None,
        'modules': modules,
        'course': course,
        'quiz': quiz,
        'quizzes': quizzes,
        'mark': mark,
         }
    return render(request, 'panel/base.html', context)


@login_required
def quiz_detail(request, quiz_id):
    quizzes = Question.objects.all()
    quiz = get_object_or_404(Quiz, id=quiz_id)
    modules = Module.objects.all()
    questions = quiz.questions.all()
    # Convert quizzes to a list and get the index of the quiz using its id
    quizzes_list = list(quizzes)
    
    try:
        quiz_index = [q.id for q in quizzes_list].index(quiz.id)
    except ValueError:
        # Handle the case when the quiz is not found in the list
        quiz_index = None
    
    context = {
        'quizzes': quizzes_list,
        'quiz': quiz,
        'modules': modules,
        'quiz_index': quiz_index,
        'questions': questions,
    }
    return render(request, 'school/quiz_detail.html', context)




