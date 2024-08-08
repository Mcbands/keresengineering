from django.db import models
# from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class library(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    # image = CloudinaryField('image')

class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField('thumbnail')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_courses_instructed', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    duration = models.CharField(max_length=40 )
    category = models.CharField(max_length=255, default="uncategorized")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    requirements = models.TextField(help_text='Enter the requirements for the course, separated by a comma.', default='')
    content = models.TextField(help_text='Enter the content for the course, separated by a comma.', default='')
    lesson_title = models.CharField(max_length=255, default='Lesson')
    students = models.ManyToManyField(User, related_name='main_enrolled_courses', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_instructor_username(self):
        return self.instructor.username
    
    def get_requirements_list(self):
        return self.requirements.split(',')

    def get_content_list(self):
        return self.content.split(',')
    
    def get_last_module_or_quiz(self):
        last_module = self.module_set.last()
        last_quiz = self.quiz_set.last()

        if last_module and last_quiz:
             return max(last_module, last_quiz, key=lambda x: x.created_at)
        elif last_module:
            return last_module
        elif last_quiz:
            return last_quiz
        else:
            return None


# class Main_Module(models.Model):
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='main_modules')

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         super().save(*args, **kwargs)

class Module(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_modules')
    # parent_module = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='submodules')
    # def __str__(self):
    #     return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def get_submodule_count(self):
    #     if self.parent_module:
    #         # If it has a parent module, get its position among the siblings
    #         position = self.parent_module.submodules.filter(id__lte=self.id).count()
    #         return f"{self.parent_module.get_submodule_count()}.{position}"
    #     else:
    #         # If it doesn't have a parent module, it's a top-level module
    #         return f"{self.id}.0"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} enrolled in {self.course.title}'



