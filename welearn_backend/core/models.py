# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('user', 'User'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
class Course(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    ratings = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # image field

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=200)
    discount = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.discount})'

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.course}'
