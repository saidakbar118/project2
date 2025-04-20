from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.generic import DetailView
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import generate_verification_code,send_sms
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import timedelta,datetime
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator



def auth_view(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    
    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.save()
                login(request, user)
                return redirect('/choice/')
        elif 'login' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                
                if user.profile.role == 'teacher':
                    return redirect('/teacherpage/')
                elif user.profile.role == 'student':
                    return redirect('/studentpage/')
                else:
                    return redirect('role_selection') 
    
    return render(request, 'registration/login.html', {'register_form': register_form, 'login_form': login_form})

@login_required
def role_selection_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        if role in ['teacher', 'student']:
            profile, created = ProfileUser.objects.get_or_create(user=request.user)

            print("Eski role:", profile.role)  # Debug uchun
            profile.role = role
            profile.save()
            print("Yangi role:", profile.role)  # Debug uchun

            if role == 'teacher':
                return redirect('/teacherregister/')
            else:
                return redirect('/studentregister/')

    return render(request, 'registration/choice.html')

@login_required
def teacher_profile_update_view(request):
    profile = request.user.profile  
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)  
        if form.is_valid():
            profile = form.save(commit=False)
            profile.role = request.user.profile.role  
            profile.save()
            return redirect('/teacherpage/')
    else:
        form = UserProfileForm(instance=profile)  
        
    return render(request, 'registration/teacher-register.html', {'form': form})

@login_required
def student_profile_update_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)  
        if form.is_valid():
            profile = form.save(commit=False)  
            profile.role = request.user.profile.role
            profile.save()
            return redirect('/studentpage/')
    else:
        form = UserProfileForm(instance=profile)  
        
    return render(request, 'registration/student-register.html', {'form': form})



def request_password_reset_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            
            try:
                user = ProfileUser.objects.get(phone_number=phone_number)
                
                verification_code = generate_verification_code()
                
                request.session['verification_code'] = verification_code
                request.session['reset_user_id'] = user.id

                message = f"Parolni tiklash uchun tasdiqlash kodi: {verification_code}"
                if send_sms(phone_number, message):
                
                    messages.success(request, f"Tasdiqlash kodi yuborildi. Iltimos, kodingizni kiriting. Username: {user.user}")
                    return redirect('/verify-code/')
                else:
                    messages.error(request, "Tasdiqlash kodini yuborishda muammo yuz berdi.")
            except ProfileUser.DoesNotExist:
                messages.error(request, "Telefon raqami tizimida topilmadi.")
    else:
        form = PhoneNumberForm()
    return render(request, 'password_reset/request_reset.html', {'form':form})
    
def verify_code_view(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('verification_code'):
                messages.success(request, "Tasdiqlash kodi to'g'ri. Endi yangi parol o'rnatishingiz mumkin.")
                return redirect('/reset-password/')
            else:
                messages.error(request, "Tasdiqlash kodi noto'g'ri.")
    else:
        form = VerificationCodeForm()
                
    return render(request, 'password_reset/verify_code.html', {'form': form})

from django.contrib.auth.hashers import make_password

def request_password_reset_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            
            try:
                user = ProfileUser.objects.get(phone_number=phone_number)
                
                verification_code = generate_verification_code()
                
                request.session['verification_code'] = verification_code
                request.session['reset_user_id'] = user.id

                message = f"Parolni tiklash uchun tasdiqlash kodi: {verification_code}"
                if send_sms(phone_number, message):
                
                    messages.success(request, f"Tasdiqlash kodi yuborildi. Iltimos, kodingizni kiriting. Username: {user.user}")
                    return redirect('/verify-code/')
                else:
                    messages.error(request, "Tasdiqlash kodini yuborishda muammo yuz berdi.")
            except ProfileUser.DoesNotExist:
                messages.error(request, "Telefon raqami tizimida topilmadi.")
    else:
        form = PhoneNumberForm()
    return render(request, 'password_reset/request_reset.html', {'form':form})
    
def verify_code_view(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('verification_code'):
                messages.success(request, "Tasdiqlash kodi to'g'ri. Endi yangi parol o'rnatishingiz mumkin.")
                return redirect('/reset-password/')
            else:
                messages.error(request, "Tasdiqlash kodi noto'g'ri.")
    else:
        form = VerificationCodeForm()
                
    return render(request, 'password_reset/verify_code.html', {'form': form})

from django.contrib.auth.hashers import make_password

def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            if user_id:
                try:
                    profile = ProfileUser.objects.get(id=user_id)  # ProfileUser ni olamiz
                    user = profile.user  # Asosiy User modelini olamiz
                    user.set_password(form.cleaned_data['new_password'])  # Parolni yangilaymiz
                    user.save()
                    messages.success(request, "Parolingiz tiklandi. Endi tizimga kiriting.")
                    return redirect('/auth/')
                except ProfileUser.DoesNotExist:
                    messages.error(request, "Foydalanuvchi topilmadi. Jarayonni qayta boshlang.")
            else:
                messages.error(request, "Sessiya tugagan. Jarayonni qayta boshlang.")
                return redirect('/request-reset/')
    else:
        form = ResetPasswordForm()
    return render(request, 'password_reset/reset_password.html', {'form': form})



@login_required
def TeacherProfileFix(request):
    profile = request.user.profile  

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect('/teacherpage/')  # Profil sahifasiga qaytarish
        else:
            print("Xatolik bor:", form.errors)  # Xatolarni tekshirish

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'teacher_profile-fix.html', {'form': form})


@login_required
def StudentProfileFix(request):
    profile = request.user.profile  

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect('/studentpage/')  # Profil sahifasiga qaytarish
        else:
            print("Xatolik bor:", form.errors)  # Xatolarni tekshirish

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'student_profile-fix.html', {'form': form})



@login_required
def TestForLecture(request, lesson_id):
    lesson = get_object_or_404(Lecture1, id=lesson_id)
    questions = LectureTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)  

    if request.method == "POST":
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = questions.count()

            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                correct_choice = None
                if question.javob == question.a_javob:
                    correct_choice = 'a'
                elif question.javob == question.b_javob:
                    correct_choice = 'b'
                elif question.javob == question.c_javob:
                    correct_choice = 'c'
                elif question.javob == question.d_javob:
                    correct_choice = 'd'

                if user_answer == correct_choice:
                    correct_answers += 1

            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            passed = percentage >= 55

            # ⭐ Yulduzlarni hisoblash
            stars_earned = 5 if passed else 0
            if percentage >= 80:
                stars_earned = 10

            # Foydalanuvchining umumiy yulduzlarini yangilash
            user_profile.stars += stars_earned  
            user_profile.save()

            # **Bugungi yulduzlarni yangilash yoki yaratish**
            if stars_earned > 0:
                today_stars, created = StarsHistory.objects.get_or_create(
                    user=request.user, date=now().date(), 
                    defaults={"stars": stars_earned}  # Agar yozuv yo‘q bo‘lsa, yaratish
                )
                if not created:  
                    today_stars.stars += stars_earned  # Agar yozuv bor bo‘lsa, yulduz qo‘shish
                    today_stars.save()

            # Foydalanuvchining test natijasini saqlaymiz
            progress, created = UserLectureProgress.objects.get_or_create(user=request.user, lesson=lesson)
            progress.passed = passed
            progress.save()

            return render(request, "tests/lecture-result.html", {
                "percentage": percentage, 
                "passed": passed, 
                "stars_earned": stars_earned,
                "lesson": lesson
            })

    else:
        form = TestForm(questions=questions)

    return render(request, "tests/lecture-test.html", {"form": form, "lesson": lesson})



@login_required
def TestForPractic(request, lesson_id):
    lesson = get_object_or_404(Practic1, id=lesson_id)
    questions = PracticTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)  

    if request.method == "POST":
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = questions.count()

            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                correct_choice = None
                if question.javob == question.a_javob:
                    correct_choice = 'a'
                elif question.javob == question.b_javob:
                    correct_choice = 'b'
                elif question.javob == question.c_javob:
                    correct_choice = 'c'
                elif question.javob == question.d_javob:
                    correct_choice = 'd'

                if user_answer == correct_choice:
                    correct_answers += 1

            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            passed = percentage >= 55

            # ⭐ Yulduzlarni hisoblash
            stars_earned = 5 if passed else 0
            if percentage >= 80:
                stars_earned = 10

            # Foydalanuvchining umumiy yulduzlarini yangilash
            user_profile.stars += stars_earned  
            user_profile.save()

            # **Bugungi yulduzlarni yangilash yoki yaratish**
            if stars_earned > 0:
                today_stars, created = StarsHistory.objects.get_or_create(
                    user=request.user, date=now().date(), 
                    defaults={"stars": stars_earned}  # Agar yozuv yo‘q bo‘lsa, yaratish
                )
                if not created:  
                    today_stars.stars += stars_earned  # Agar yozuv bor bo‘lsa, yulduz qo‘shish
                    today_stars.save()

            # Foydalanuvchining test natijasini saqlash
            progress, created = UserPracticProgress.objects.get_or_create(user=request.user, lesson=lesson)
            progress.passed = passed
            progress.save()

            return render(request, "tests/practic-result.html", {
                "percentage": percentage, 
                "passed": passed, 
                "stars_earned": stars_earned,
                "lesson": lesson
            })

    else:
        form = TestForm(questions=questions)

    return render(request, "tests/practic-test.html", {"form": form, "lesson": lesson})




@login_required
def TestForLaboratory(request, lesson_id):
    lesson = get_object_or_404(Laboratory1, id=lesson_id)
    questions = LaboratoryTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)  

    if request.method == "POST":
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = questions.count()

            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                correct_choice = None
                if question.javob == question.a_javob:
                    correct_choice = 'a'
                elif question.javob == question.b_javob:
                    correct_choice = 'b'
                elif question.javob == question.c_javob:
                    correct_choice = 'c'
                elif question.javob == question.d_javob:
                    correct_choice = 'd'

                if user_answer == correct_choice:
                    correct_answers += 1

            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            passed = percentage >= 55

            # ⭐ Yulduzlarni hisoblash
            stars_earned = 5 if passed else 0
            if percentage >= 80:
                stars_earned = 10

            # Foydalanuvchining umumiy yulduzlarini yangilash
            user_profile.stars += stars_earned  
            user_profile.save()

            # **Bugungi yulduzlarni yangilash yoki yaratish**
            if stars_earned > 0:
                today_stars, created = StarsHistory.objects.get_or_create(
                    user=request.user, date=now().date(), 
                    defaults={"stars": stars_earned}  
                )
                if not created:  
                    today_stars.stars += stars_earned  
                    today_stars.save()

            # Foydalanuvchining test natijasini saqlash
            progress, created = UserLaboratoryProgress.objects.get_or_create(user=request.user, lesson=lesson)
            progress.passed = passed
            progress.save()

            return render(request, "tests/laboratory-result.html", {
                "percentage": percentage, 
                "passed": passed, 
                "stars_earned": stars_earned,
                "lesson": lesson
            })

    else:
        form = TestForm(questions=questions)

    return render(request, "tests/laboratory-test.html", {"form": form, "lesson": lesson})




def Entrance(request):
    return render(request,'entrance.html')



def Success(request):
    return render(request,'registration/success.html')


def TeacherPage(request):
    context={
        'teacher':TeacherPage1.objects.all(),
    }
    return render(request,'teacher-page.html',context)

def StudentPage(request):
    context={
        'student':StudentPage1.objects.all(),
    }
    return render(request,'student-page.html',context)

def Profile(request):
    context={
        'profile':Profile1.objects.all(),
    }
    return render(request,'profile.html',context)


def Objects(request):
    context={
        'objects':Objects1.objects.all(),
    }
    return render(request,'sahifalar/objects.html',context)


def Lecture(request):
    user = request.user
    lectures = Lecture1.objects.all().order_by('maruza_raqam')

    for lecture in lectures:
        if lecture.maruza_raqam == 1:  
            lecture.previous_lecture_passed = True  # Birinchi dars ochiq
        else:
            prev_lesson = Lecture1.objects.filter(maruza_raqam=lecture.maruza_raqam - 1).first()
            lecture.previous_lecture_passed = UserLectureProgress.objects.filter(
                user=user, 
                lesson=prev_lesson, 
                passed=True
            ).exists()

    context = {
        'lectureback': LectureBack.objects.all(),
        'lecture': lectures,
    }
    return render(request, 'fanlar/lecture.html', context)

def can_access_lesson(user, lesson):
    """Foydalanuvchi faqat oldingi dars testini topshirgan bo‘lsa, ruxsat beriladi."""
    if int(lesson.maruza_raqam) == 1:  # Birinchi dars har doim ochiq
        return True

    prev_lesson = Lecture1.objects.filter(maruza_raqam=str(int(lesson.maruza_raqam) - 1)).first()

    return UserLectureProgress.objects.filter(
        user=user, 
        lesson=prev_lesson, 
        passed=True
    ).exists()

@method_decorator(login_required, name='dispatch')
class LectureDetail(DetailView):
    model = Lecture1
    template_name = 'lecture-detail.html'
    context_object_name = 'lecturedet'

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()

        if not can_access_lesson(request.user, lesson):
            return render(request, 'fanlar/403-forbidden.html', status=403)  # 403-хатолик саҳифасини рендер қилиш

        return super().dispatch(request, *args, **kwargs)
    
    
def Practic(request):
    user = request.user
    practics = Practic1.objects.all().order_by('practic_raqam')

    for practic in practics:
        if practic.practic_raqam == 1:  
            practic.previous_practic_passed = True  # Birinchi amaliyot ochiq
        else:
            prev_practic = Practic1.objects.filter(practic_raqam=practic.practic_raqam - 1).first()
            practic.previous_practic_passed = UserPracticProgress.objects.filter(
                user=user, 
                lesson=prev_practic, 
                passed=True
            ).exists()

    context = {
        'lectureback': LectureBack.objects.all(),
        'practic': practics,
    }
    return render(request, 'fanlar/practic.html', context)


def can_access_practic(user, lesson):
    """Foydalanuvchi faqat oldingi amaliyot testini topshirgan bo‘lsa, ruxsat beriladi."""
    if int(lesson.practic_raqam) == 1:  # Birinchi dars har doim ochiq
        return True

    prev_lesson = Practic1.objects.filter(practic_raqam=str(int(lesson.practic_raqam) - 1)).first()

    return UserPracticProgress.objects.filter(
        user=user, 
        lesson=prev_lesson, 
        passed=True
    ).exists()
    
    
@method_decorator(login_required, name='dispatch')
class PracticDetail(DetailView):
    model = Practic1
    template_name = 'practic-detail.html'
    context_object_name = 'practicdet'

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()

        if not can_access_practic(request.user, lesson):
            return render(request, 'fanlar/403-forbidden.html', status=403)  # 403-xatolik sahifasini ko‘rsatish

        return super().dispatch(request, *args, **kwargs)
    
    
def Laboratory(request):
    user = request.user
    laboratories = Laboratory1.objects.all().order_by('laboratory_raqam')

    for laboratory in laboratories:
        if laboratory.laboratory_raqam == 1:  
            laboratory.previous_laboratory_passed = True  # Birinchi laboratoriya ochiq
        else:
            prev_laboratory = Laboratory1.objects.filter(laboratory_raqam=laboratory.laboratory_raqam - 1).first()
            laboratory.previous_laboratory_passed = UserLaboratoryProgress.objects.filter(
                user=user, 
                lesson=prev_laboratory, 
                passed=True
            ).exists()

    context = {
        'lectureback': LectureBack.objects.all(),
        'laboratory': laboratories,
    }
    return render(request, 'fanlar/laboratory.html', context)

def can_access_laboratory(user, lesson):
    """Foydalanuvchi faqat oldingi laboratoriya testini topshirgan bo‘lsa, ruxsat beriladi."""
    if int(lesson.laboratory_raqam) == 1:  # Birinchi dars har doim ochiq
        return True

    prev_lesson = Laboratory1.objects.filter(laboratory_raqam=str(int(lesson.laboratory_raqam) - 1)).first()

    return UserLaboratoryProgress.objects.filter(
        user=user, 
        lesson=prev_lesson, 
        passed=True
    ).exists()

@method_decorator(login_required, name='dispatch')
class LaboratoryDetail(DetailView):
    model = Laboratory1
    template_name = 'laboratory-detail.html'
    context_object_name = 'laboratorydet'

    def dispatch(self, request, *args, **kwargs):
        lesson = self.get_object()

        if not can_access_laboratory(request.user, lesson):
            return render(request, 'fanlar/403-forbidden.html', status=403)  # 403-xatolik sahifasini ko‘rsatish

        return super().dispatch(request, *args, **kwargs)
   

    
def Selfstudy(request):
    context={
        'selfstudy':Selfstudy1.objects.all(),
    }
    return render(request,'fanlar/selfstudy.html',context)

def Trio(request):
    context={
        'trio':Trio1.objects.all(),
    }
    return render(request,'sahifalar/trio.html',context)

def Bilim(request):
    context={
        'bilim':Bilim1.objects.all(),
    }
    return render(request,'sahifalar/bilim.html',context)

def TrioStudent(request):
    context={
        'trio':Trio1.objects.all(),
    }
    return render(request,'sahifalar/trio-student.html',context)



def activity_page(request):
    return render(request, "active.html")

@login_required
def get_activity_data(request):
    """ Foydalanuvchining haftalik faollik vaqtlarini qaytaradi """
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Dushanbadan boshlab
    days = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"]

    activity_data = {day: 0 for day in days}  # Default 0 soat
    
    activities = UserActivity.objects.filter(
        user=request.user, date__gte=start_of_week
    )
    
    for activity in activities:
        weekday = activity.date.weekday()
        activity_data[days[weekday]] = activity.duration

    return JsonResponse(activity_data)

def log_activity(request):
    """ Foydalanuvchi sahifada bo'lsa, faollik vaqtini qo‘shadi """
    if request.user.is_authenticated:
        today = now().date()
        activity, created = UserActivity.objects.get_or_create(user=request.user, date=today)

        # Oxirgi marta yangilangani bilan hozirgi vaqt orasidagi farq (daqiqa)
        time_since_last_update = (now() - activity.updated_at).total_seconds() / 60 
        
        if time_since_last_update >= 1:  # Faqat 5 daqiqadan keyin qo‘shish
            activity.duration += 1  # 1 daqiqa qo‘shish
            activity.save()

    return JsonResponse({"status": "updated", "new_duration": activity.duration})




from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models import Count
from datetime import datetime, timedelta

def Chart(request):
    return render(request, "chart.html")

@receiver(user_logged_in)
def log_user_activity(sender, request, user, **kwargs):
    today = now().date()
    UserChart.objects.get_or_create(user=user, date=today)
    
def weekly_user_count(request):
    """ Har kuni nechta unikal foydalanuvchi kirganini hisoblaydi """
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Dushanbadan boshlab

    user_activity = UserChart.objects.filter(date__gte=start_of_week) \
        .values('date') \
        .annotate(count=Count('user', distinct=True))  # Unikal userlarni sanaymiz

    # Ma’lumotni tayyorlash
    days = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"]
    result = {day: 0 for day in days}

    for entry in user_activity:
        weekday = entry['date'].weekday()  # 0 - Dushanba, 6 - Yakshanba
        result[days[weekday]] = entry['count']

    return JsonResponse({"days": list(result.keys()), "counts": list(result.values())})



def Stars(request):
    user_profile = ProfileUser.objects.get(user=request.user)
    return render(request, "stars.html", {"stars": user_profile.stars})

def StarsDaily(request):
    today = now().date()
    today_stars = StarsHistory.objects.filter(user=request.user, date=today).aggregate(models.Sum("stars"))["stars__sum"] or 0
    return render(request, "stars-daily.html", {"today_stars": today_stars})

def Home(request):
    return render(request,"sahifalar/home.html")

def TeacherContact(request):
    return render(request,"header/teacher-contact.html")

def StudentContact(request):
    return render(request,"header/student-contact.html")

def AdminContact(request):
    context={
        'admin':Admin_Contact.objects.all(),
    }
    return render(request,"header/admin-contact.html",context)

def Notifications(request):
    return render(request,"header/notifications.html")

def AboutUs(request):
    context = {
        "text":about_us_model.objects.all(),
    }
    return render(request,"about-us.html",context)


def suniy_intelekt(request):
    return render(request,"sahifalar/suniy.html")

def media_view(request):
    context={
        'admin':Admin_Contact.objects.all(),
    }
    return render(request,"media.html",context)

#notifications

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sender_profile = ProfileUser.objects.get(user=request.user)
        receiver_profile = ProfileUser.objects.get(id=data["receiver_id"])  # `id` orqali topamiz
        text = data["text"]
        
        Message.objects.create(sender=sender_profile, receiver=receiver_profile, text=text)
        return JsonResponse({"status": "success", "message": "Xabar yuborildi!"})

def get_students(request):
    students = ProfileUser.objects.filter(role="student").values("id", "full_name", "phone_number")
    return JsonResponse({"students": list(students)})

def get_notifications(request):
    """Yangi xabarlarni JSON formatida qaytaradi"""
    user_profile = ProfileUser.objects.get(user=request.user)
    messages = Message.get_recent_messages(user_profile)

    notifications = [
        {
            "id": msg.id,
            "sender": msg.sender.full_name, 
            "text": msg.text, 
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for msg in messages
    ]
    
    return JsonResponse({"notifications": notifications})

@csrf_exempt
def mark_notification_as_read(request):
    """Bitta xabarni o‘qilgan deb belgilash"""
    if request.method == "POST":
        data = json.loads(request.body)
        message_id = data.get("message_id")
        try:
            message = Message.objects.get(id=message_id)
            message.is_read = True
            message.save()
            return JsonResponse({"status": "success", "message": "Xabar o‘qildi!"})
        except Message.DoesNotExist:
            return JsonResponse({"error": "Xabar topilmadi"}, status=404)

@csrf_exempt
def send_teacher_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sender_profile = ProfileUser.objects.get(user=request.user)
        receiver_profile = ProfileUser.objects.get(id=data["receiver_id"])  # `id` orqali topamiz
        text = data["text"]
        
        Message.objects.create(sender=sender_profile, receiver=receiver_profile, text=text)
        return JsonResponse({"status": "success", "message": "Xabar yuborildi!"})
    
# Teacher ro‘yxatini olish
def get_teachers(request):
    teachers = ProfileUser.objects.filter(role="teacher").values("id", "full_name", "phone_number")
    return JsonResponse({"teachers": list(teachers)})


def get_unread_notifications(request):
    user_profile = ProfileUser.objects.get(user=request.user)
    unread_count = Message.objects.filter(receiver=user_profile, is_read=False).count()
    return JsonResponse({"unread_count": unread_count})


@csrf_exempt
def mark_notification_as_read(request):
    """Xabarni o‘qilgan deb belgilash"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message_id = data.get("message_id")

            message = Message.objects.get(id=message_id)
            message.is_read = True
            message.save()

            return JsonResponse({"status": "success", "message": "Xabar o‘qildi!"})
        except Message.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Xabar topilmadi"}, status=404)
    return JsonResponse({"status": "error", "message": "Noto‘g‘ri so‘rov"}, status=400)


#sinfxona

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Lesson

def teacher_page(request):
    """ Teacher sahifasi - Stream yaratish """
    if request.method == "POST":
        title = request.POST.get("title")
        meet_link = request.POST.get("meet_link")  # Google Meet link
        lesson = Lesson.objects.create(title=title, meet_link=meet_link)
        return redirect("teacher_page")

    lessons = Lesson.objects.filter(is_active=True)
    return render(request, "sahifalar/teacher.html", {"lessons": lessons})

def student_page(request):
    """ Student sahifasi - Mavjud streamlarni ko‘rish """
    lessons = Lesson.objects.filter(is_active=True)
    return render(request, "sahifalar/student.html", {"lessons": lessons})

def end_stream(request, lesson_id):
    """ Streamni tugatish """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.is_active = False
    lesson.save()
    return JsonResponse({"message": "Stream Ended"})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import UserExamAttempt, ExamTest

@login_required
def start_exam(request):
    # Foydalanuvchining testga bo'lgan harakatlarini olish yoki yaratish
    user_attempt, created = UserExamAttempt.objects.get_or_create(user=request.user)

    # Agar foydalanuvchi allaqachon testni o'tgan bo'lsa
    if user_attempt.passed:
        return render(request, "tests/exam-passed.html")

    # Agar foydalanuvchi ikki marta sinab ko'rgan bo'lsa, testni bloklash
    if user_attempt.attempt_count >= 2:
        return render(request, "tests/exam-blocked.html")

    # Agar test boshlanmagan yoki vaqt tugagan bo'lsa, testni boshlash
    if user_attempt.start_time is None or user_attempt.is_time_over():
        user_attempt.start_exam()

    # Test savollarini olish
    questions = ExamTest.objects.all()

    # Agar so'rov POST bo'lsa, testni baholash
    if request.method == "POST":
        correct_answers = 0
        total_questions = questions.count()

        # Foydalanuvchi javoblarini tekshirish
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                correct_answers += 1

        # To'g'ri javoblar foizini hisoblash
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        passed = percentage >= 55  # Testdan o‘tish uchun 55% to'g'ri javob kerak

        # Agar foydalanuvchi testni o'tgan bo'lsa
        if passed:
            user_attempt.passed = True
            user_attempt.save()
            return render(request, "tests/exam-result.html", {
                "passed": passed,
                "percentage": percentage,
                "message": "Tabriklaymiz! Siz testdan o‘tdingiz! 🎉",
                "stop_timer": True
            })

        # Agar foydalanuvchi testni o'ta olmagan bo'lsa
        user_attempt.attempt_count += 1
        user_attempt.save()

        # Ikkinchi urinishdan keyin testni bloklash
        if user_attempt.attempt_count == 2:
            return render(request, "tests/exam-result.html", {
                "passed": passed, 
                "percentage": percentage,
                "message": "Afsuski, siz testdan o‘ta olmadingiz. Endi sizda test topshirish imkoniyati yo‘q.",
                "stop_timer": True
            })

        # Testni qayta topshirishga ruxsat berish
        return render(request, "tests/exam-result.html", {
            "passed": passed, 
            "percentage": percentage,
            "message": "Afsuski, siz testdan o‘ta olmadingiz. Yana bir bor urinib ko‘rishingiz mumkin.",
            "stop_timer": True
        })

    # Testni boshlash uchun sahifani render qilish
    return render(request, "tests/exam.html", {
        "questions": questions, 
        "user_attempt": user_attempt,
        "end_time": user_attempt.end_time.timestamp() if not user_attempt.passed else None
    })






