from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserRole(models.TextChoices):
    STUDENT = 'ST', 'Student'
    PARENT = 'PA', 'Parent'
    TEACHER = 'TC', 'Teacher'
    ADMIN = 'AD', 'Admin'

class Colors(models.TextChoices):
    RED = 'R', 'Red'
    BLUE = 'B', 'Blue'
    GREEN = 'G', 'Green'
    YELLOW = 'Y', 'Yellow'
    ORANGE = 'O', 'Orange'
    PURPLE = 'P', 'Purple'
    WHITE = 'W', 'White'

class User(AbstractUser):
    role = models.CharField(max_length=2, choices=UserRole.choices, default=UserRole.STUDENT)

    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    avatar = models.ImageField(upload_to='assets/avatars/', blank=True, null=True)

    def is_student(self):
        return self.role == UserRole.STUDENT

    def is_teacher(self):
        return self.role == UserRole.TEACHER

    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def is_parent(self):
        return self.role == UserRole.PARENT
    
class Student(User):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    current_grade = models.IntegerField(blank=True, null=True)
    guardian = models.ForeignKey('Parent', on_delete=models.CASCADE)

class Teacher(User):
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
    pass

class Parent(User):
    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    pass

@receiver(post_save, sender=User)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.role = UserRole.ADMIN
        instance.save()

class Attachment(models.Model): 
    file = models.FileField(upload_to='assets/attachments/')
    name = models.CharField(max_length=255, blank=True, null=True)

class Course(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=2, choices=Colors.choices, default=Colors.WHITE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    due_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    points = models.IntegerField()
    max_points = models.IntegerField()

    attachments = models.ManyToManyField('Attachment', blank=True)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    attachments = models.ManyToManyField('Attachment', blank=True)

    grade = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    submitted = models.BooleanField(default=False)
    submittedAt = models.DateTimeField(blank=True, null=True)

class Event(models.Model):
    title = models.CharField(max_length=255, blank=True)

    start = models.DateTimeField()
    end = models.DateTimeField()

    color = models.CharField(max_length=2, choices=Colors.choices, default=Colors.WHITE)

class Lesson(Event):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)