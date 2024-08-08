from django.db import models
from django.contrib.auth.models import User
from main.models import Module,Course
import random


from django.utils import timezone
import uuid







DIFF_CHOICES = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard')
)

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the quiz in minutes")
    score_to_pass = models.IntegerField(help_text="Score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quiz_module')
    is_completed = models.BooleanField(default=False)  # New field to track quiz completion

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    class Meta:
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    text = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct} "
     

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.pk)

