# Generated by Django 4.2.2 on 2024-02-14 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_module_parent_module_delete_main_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='featured_video',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lesson_video',
        ),
        migrations.AlterField(
            model_name='course',
            name='content',
            field=models.TextField(default='', help_text='Enter the content for the course, separated by a comma.'),
        ),
    ]
