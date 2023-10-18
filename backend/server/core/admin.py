from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)

admin.site.register(Attachment)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)

admin.site.register(Event)
admin.site.register(Lesson)