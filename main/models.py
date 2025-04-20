from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import  timedelta


class ProfileUser(models.Model):
    ROLE_CHOICES = [
        ('teacher', "O'qituvchi"),
        ('student', "Talaba"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  
    full_name = models.CharField(max_length=100)
    workplace = models.CharField(max_length=150, blank=True, null=True)  # O‘qituvchilar uchun
    faculty = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)  # Talabalar uchun
    specialization = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=13)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,null=True,blank=True,default='student')
    birthdate = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
   
class ProfileInline(admin.StackedInline):  # Inline admin
    model = ProfileUser
    can_delete = False  # Profilni alohida o‘chirishga yo‘l qo‘ymaslik
    verbose_name_plural = "Profile"

class CustomUserAdmin(UserAdmin):  # UserAdmin'ni o‘zgartiramiz
    inlines = [ProfileInline] 
    
    
from django.utils.timezone import now

class StarsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    date = models.DateField(default=now)
    
    
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.FloatField(default=0)  # Daqiqalar bilan hisoblanadi
    updated_at = models.DateTimeField(auto_now=True) 


class UserChart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)  # Foydalanuvchi kirgan sana


class TeacherPage1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()
    image6 = models.ImageField()
    image7 = models.ImageField()
    image8 = models.ImageField()
    image9 = models.ImageField()
    image10 = models.ImageField()
    image11 = models.ImageField()

    
    
class StudentPage1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()
    image6 = models.ImageField()
    image7 = models.ImageField()
    image8 = models.ImageField()
    image9 = models.ImageField()
    image10 = models.ImageField()
    image11 = models.ImageField()
    
class Profile1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()
    image6 = models.ImageField()
    image7 = models.ImageField()
    image8 = models.ImageField()
    image9 = models.ImageField() 
    
class Objects1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()
    image4 = models.ImageField()
    image5 = models.ImageField()  
    
    
class ProfileFix1(models.Model):
    image = models.ImageField()
    
class LectureBack(models.Model):
    image1 = models.ImageField()  
    
from ckeditor_uploader.fields import RichTextUploadingField
    

class Lecture1(models.Model):
    maruza_video = models.FileField(null=True,blank=True)
    maruza_raqam = models.IntegerField()
    maruza_nomi = models.CharField(max_length=150)
    maruza_matni = RichTextUploadingField()  



class Practic1(models.Model):
    practic_video = models.FileField()
    practic_raqam = models.IntegerField()
    practic_nomi = models.CharField(max_length=150)
    practic_matni = models.TextField()
    
class Laboratory1(models.Model):
    laboratory_video = models.FileField()
    laboratory_raqam = models.IntegerField()
    laboratory_nomi = models.CharField(max_length=150)
    laboratory_matni = models.TextField()
    
class Selfstudy1(models.Model):
    mustaqiltalim_matni = models.TextField()
    
    
class UserLectureProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lecture1", on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

class UserPracticProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Practic1", on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)

class UserLaboratoryProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Laboratory1", on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)


class Trio1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()  
    image4 = models.ImageField()  
    image5 = models.ImageField()
    
class Bilim1(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()  
    image4 = models.ImageField()  
    

class LectureTest(models.Model):
    lesson = models.ForeignKey(Lecture1,on_delete=models.CASCADE)
    savol = models.TextField()
    a_javob = models.CharField(max_length=200)
    b_javob = models.CharField(max_length=200)
    c_javob = models.CharField(max_length=200)
    d_javob = models.CharField(max_length=200)
    javob = models.CharField(max_length=200)
    
    
class PracticTest(models.Model):
    lesson = models.ForeignKey(Practic1,on_delete=models.CASCADE)
    savol = models.TextField()
    a_javob = models.CharField(max_length=200)
    b_javob = models.CharField(max_length=200)
    c_javob = models.CharField(max_length=200)
    d_javob = models.CharField(max_length=200)
    javob = models.CharField(max_length=200)
    
class LaboratoryTest(models.Model):
    lesson = models.ForeignKey(Laboratory1,on_delete=models.CASCADE)
    savol = models.TextField()
    a_javob = models.CharField(max_length=200)
    b_javob = models.CharField(max_length=200)
    c_javob = models.CharField(max_length=200)
    d_javob = models.CharField(max_length=200)
    javob = models.CharField(max_length=200)
    
    
class Admin_Contact(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()            
    image3 = models.ImageField()
    extra_image = models.ImageField()
    
    
class Message(models.Model):
    sender = models.ForeignKey('ProfileUser', on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey('ProfileUser', on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}: {self.text[:30]}"

    @classmethod
    def get_recent_messages(cls, user_profile):
        last_24_hours = now() - timedelta(hours=24)
        return cls.objects.filter(receiver=user_profile, timestamp__gte=last_24_hours, is_read=False)
    

class Lesson(models.Model):
    title = models.CharField(max_length=200)  # Dars nomi
    meet_link = models.URLField()  # Google Meet havolasi
    is_active = models.BooleanField(default=True)  # Stream holati

    def __str__(self):
        return self.title
    

class about_us_model(models.Model):
    text = RichTextUploadingField()  
    

from django.utils import timezone  
  
class ExamTest(models.Model):
    question = models.TextField()
    a_option = models.CharField(max_length=200)
    b_option = models.CharField(max_length=200)
    c_option = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])

class UserExamAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempt_count = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def start_exam(self):
        self.start_time = timezone.now()
        self.end_time = self.start_time + timedelta(minutes=40)  # Taymerni 40 daqiqa qilib sozlash
        self.save()

    def is_time_over(self):
        return timezone.now() > self.end_time  # Vaqt o‘tgandan keyin testni yopish



    
    