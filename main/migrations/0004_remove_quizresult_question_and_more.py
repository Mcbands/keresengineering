# Generated by Django 4.2.2 on 2024-02-09 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_question_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizresult',
            name='question',
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='selected_choice',
        ),
        migrations.RemoveField(
            model_name='quizresult',
            name='user',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='QuizResult',
        ),
    ]