# Generated by Django 4.2.2 on 2024-02-09 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_quizresult_question_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='associated_module',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
