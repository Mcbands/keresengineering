from django.db import models

STATUS_CHOICE = (("Draft", "Draft"), ("Published", "Published"))
# Create your models here.
class Book(models.Model):
    FORMAT_CHOICES = [
        ("HC", 'Hardcover'),
        ('EB', 'Ebook'),
        ('Au','Audiobook'),
    ]
    title = models.CharField(max_length=500)
    cover_image = models.ImageField(upload_to="ebook")
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    short_description = models.TextField(max_length=2000)
    price = models.IntegerField()
    publiction_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")

    def __str__(self):
        return self.title