from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db import models

admin.site.register(TeacherPage1)
admin.site.register(StudentPage1)
admin.site.register(Profile1)
admin.site.register(ProfileFix1)
admin.site.register(Objects1)
admin.site.register(LectureBack)
admin.site.register(Practic1)
admin.site.register(Laboratory1)
admin.site.register(Selfstudy1)
admin.site.register(Trio1)
admin.site.register(Bilim1)
admin.site.register(LectureTest)
admin.site.register(PracticTest)
admin.site.register(LaboratoryTest)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(StarsHistory)
admin.site.register(Admin_Contact)
admin.site.register(Lesson)
admin.site.register(about_us_model)
admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(UserExamAttempt)



class Lecture1Admin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }

admin.site.register(Lecture1, Lecture1Admin)


