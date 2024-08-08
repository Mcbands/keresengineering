# Generated by Django 4.2.2 on 2024-02-03 14:46

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='', verbose_name='thumbnail')),
                ('featured_video', models.FileField(upload_to='featured_videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=20)),
                ('duration', models.CharField(default='0', max_length=10)),
                ('category', models.CharField(default='uncategorized', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('requirements', models.TextField(default='', help_text='Enter the requirements for the course, separated by a comma.')),
                ('content', models.TextField(default='', help_text='Enter the course content, separated by a comma.')),
                ('lesson_title', models.CharField(default='Lesson', max_length=255)),
                ('lesson_video', ckeditor.fields.RichTextField(null=True, verbose_name='lesson_video')),
                ('instructor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='main_courses_instructed', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='main_enrolled_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_modules', to='main.course')),
                ('parent_module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submodules', to='main.module')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('passing_score', models.IntegerField()),
                ('duration_minutes', models.IntegerField()),
                ('associated_module', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='associated_test', to='main.module')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time_limit_minutes', models.IntegerField()),
                ('content', ckeditor.fields.RichTextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='main.course')),
            ],
        ),
        migrations.CreateModel(
            name='Main_Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_modules', to='main.course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_enrollments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
