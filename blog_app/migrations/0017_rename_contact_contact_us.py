# Generated by Django 4.2.2 on 2024-02-07 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0016_rename_subject_contact_phone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='Contact_Us',
        ),
    ]