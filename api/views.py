from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, get_user_model
from .serializers import *
from main.utils import generate_verification_code, send_sms
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                "message": "User registered successfully.",
                "token": token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                "message": "Login successful.",
                "token": token.key,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleSelectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoleSelectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response({"message": "Role selected successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile, created = ProfileUser.objects.get_or_create(user=user)

        if profile.role != 'teacher':
            return Response({"error": "Faqat o'qituvchilar ushbu ma'lumotni yangilay olishadi."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TeacherProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "O'qituvchi profili muvaffaqiyatli yangilandi."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile, created = ProfileUser.objects.get_or_create(user=user)

        if profile.role != 'student':
            return Response({"error": "Faqat talabalar ushbu ma'lumotni yangilay olishadi."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudentProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Talaba profili muvaffaqiyatli yangilandi."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Telefon raqam kiritilmadi."}, status=400)
        
        try:
            user_profile = ProfileUser.objects.get(phone_number=phone_number)
            code = generate_verification_code()

            request.session['reset_code'] = code
            request.session['reset_user_id'] = user_profile.id

            message = f"Parolni tiklash uchun kod: {code}"
            send_sms(phone_number, message)

            return Response({
                "message": "Tasdiqlash kodi yuborildi.",
                "username": user_profile.user.username
            }, status=200)

        except ProfileUser.DoesNotExist:
            return Response({"error": "Bu raqamga mos foydalanuvchi topilmadi."}, status=404)
        
class VerifyCodeAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code')
        saved_code = request.session.get('reset_code')

        if code == saved_code:
            return Response({"message": "Kod to'g'ri."}, status=200)
        else:
            return Response({"error": "Kod noto‘g‘ri."}, status=400)

class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        new_password = request.data.get('new_password')
        user_id = request.session.get('reset_user_id')

        if not user_id:
            return Response({"error": "Sessiya muddati tugagan. Jarayonni qayta boshlang."}, status=400)

        try:
            profile = ProfileUser.objects.get(id=user_id)
            user = profile.user
            user.set_password(new_password)
            user.save()

            # Sessiyani tozalash
            request.session.pop('reset_code', None)
            request.session.pop('reset_user_id', None)

            return Response({"message": "Parol muvaffaqiyatli tiklandi."}, status=200)
        except ProfileUser.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=404)
        
        
class TeacherProfileUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = TeacherProfileUpdateSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = TeacherProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Profil yangilandi'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = StudentProfileUpdateSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = StudentProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Profil yangilandi'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_test(request, lesson_id):
    lesson = get_object_or_404(Lecture1, id=lesson_id)
    tests = LectureTest.objects.filter(lesson=lesson)
    serializer = LectureTestSerializer(tests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_lecture_test(request, lesson_id):
    lesson = get_object_or_404(Lecture1, id=lesson_id)
    questions = LectureTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)

    answers = request.data.get('answers', {})  # JSON body: {'answers': {'1': 'a', '2': 'c', ...}}

    correct = 0
    for q in questions:
        user_ans = answers.get(str(q.id))
        correct_choice = ''
        if q.javob == q.a_javob:
            correct_choice = 'a'
        elif q.javob == q.b_javob:
            correct_choice = 'b'
        elif q.javob == q.c_javob:
            correct_choice = 'c'
        elif q.javob == q.d_javob:
            correct_choice = 'd'

        if user_ans == correct_choice:
            correct += 1

    total = questions.count()
    percentage = (correct / total) * 100 if total > 0 else 0
    passed = percentage >= 55
    stars_earned = 10 if percentage >= 80 else 5 if passed else 0

    # ⭐ Update stars
    user_profile.stars += stars_earned
    user_profile.save()

    # ⭐ Update StarsHistory
    if stars_earned > 0:
        today_stars, created = StarsHistory.objects.get_or_create(
            user=request.user, date=now().date(),
            defaults={'stars': stars_earned}
        )
        if not created:
            today_stars.stars += stars_earned
            today_stars.save()

    # ✅ Save progress
    progress, _ = UserLectureProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.passed = passed
    progress.save()

    return Response({
        'correct_answers': correct,
        'total_questions': total,
        'percentage': percentage,
        'passed': passed,
        'stars_earned': stars_earned
    })
    
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_practic_test(request, lesson_id):
    lesson = get_object_or_404(Practic1, id=lesson_id)
    tests = PracticTest.objects.filter(lesson=lesson)
    serializer = PracticTestSerializer(tests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_practic_test(request, lesson_id):
    lesson = get_object_or_404(Practic1, id=lesson_id)
    questions = PracticTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)

    answers = request.data.get('answers', {})  # JSON body: {'answers': {'1': 'a', '2': 'c', ...}}

    correct = 0
    for q in questions:
        user_ans = answers.get(str(q.id))
        correct_choice = ''
        if q.javob == q.a_javob:
            correct_choice = 'a'
        elif q.javob == q.b_javob:
            correct_choice = 'b'
        elif q.javob == q.c_javob:
            correct_choice = 'c'
        elif q.javob == q.d_javob:
            correct_choice = 'd'

        if user_ans == correct_choice:
            correct += 1

    total = questions.count()
    percentage = (correct / total) * 100 if total > 0 else 0
    passed = percentage >= 55
    stars_earned = 10 if percentage >= 80 else 5 if passed else 0

    # ⭐ Update stars
    user_profile.stars += stars_earned
    user_profile.save()

    # ⭐ Update StarsHistory
    if stars_earned > 0:
        today_stars, created = StarsHistory.objects.get_or_create(
            user=request.user, date=now().date(),
            defaults={'stars': stars_earned}
        )
        if not created:
            today_stars.stars += stars_earned
            today_stars.save()

    # ✅ Save progress
    progress, _ = UserPracticProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.passed = passed
    progress.save()

    return Response({
        'correct_answers': correct,
        'total_questions': total,
        'percentage': percentage,
        'passed': passed,
        'stars_earned': stars_earned
    })
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_laboratory_test(request, lesson_id):
    lesson = get_object_or_404(Laboratory1, id=lesson_id)
    tests = LaboratoryTest.objects.filter(lesson=lesson)
    serializer = LaboratoryTestSerializer(tests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_laboratory_test(request, lesson_id):
    lesson = get_object_or_404(Laboratory1, id=lesson_id)
    questions = LaboratoryTest.objects.filter(lesson=lesson)
    user_profile = ProfileUser.objects.get(user=request.user)

    answers = request.data.get('answers', {})  # JSON body: {'answers': {'1': 'a', '2': 'c', ...}}

    correct = 0
    for q in questions:
        user_ans = answers.get(str(q.id))
        correct_choice = ''
        if q.javob == q.a_javob:
            correct_choice = 'a'
        elif q.javob == q.b_javob:
            correct_choice = 'b'
        elif q.javob == q.c_javob:
            correct_choice = 'c'
        elif q.javob == q.d_javob:
            correct_choice = 'd'

        if user_ans == correct_choice:
            correct += 1

    total = questions.count()
    percentage = (correct / total) * 100 if total > 0 else 0
    passed = percentage >= 55
    stars_earned = 10 if percentage >= 80 else 5 if passed else 0

    # ⭐ Update stars
    user_profile.stars += stars_earned
    user_profile.save()

    # ⭐ Update StarsHistory
    if stars_earned > 0:
        today_stars, created = StarsHistory.objects.get_or_create(
            user=request.user, date=now().date(),
            defaults={'stars': stars_earned}
        )
        if not created:
            today_stars.stars += stars_earned
            today_stars.save()

    # ✅ Save progress
    progress, _ = UserLaboratoryProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.passed = passed
    progress.save()

    return Response({
        'correct_answers': correct,
        'total_questions': total,
        'percentage': percentage,
        'passed': passed,
        'stars_earned': stars_earned
    })  
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_images(request):
    images = TeacherPage1.objects.all()
    serializer = TeacherPage1Serializer(images, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_images(request):
    images = StudentPage1.objects.all()
    serializer = StudentPage1Serializer(images, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_images(request):
    images = Profile1.objects.all()
    serializer = Profile1Serializer(images, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_objects_images(request):
    images = Objects1.objects.all()
    serializer = ObjectsSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecture_list(request):
    lectures = Lecture1.objects.all().order_by('maruza_raqam')
    serializer = LectureListSerializer(lectures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecture_detail(request, pk):
    try:
        lecture = Lecture1.objects.get(pk=pk)
    except Lecture1.DoesNotExist:
        return Response({'error': 'Lecture not found'}, status=404)

    serializer = LectureDetailSerializer(lecture, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def practic_list(request):
    practics = Practic1.objects.all().order_by('practic_raqam')
    serializer = PracticListSerializer(practics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def practic_detail(request, pk):
    try:
        practic = Practic1.objects.get(pk=pk)
    except Practic1.DoesNotExist:
        return Response({'error': 'Practic not found'}, status=404)

    serializer = PracticDetailSerializer(practic, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def laboratory_list(request):
    laboratorys = Laboratory1.objects.all().order_by('laboratory_raqam')
    serializer = LaboratoryListSerializer(laboratorys, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def laboratory_detail(request, pk):
    try:
        laboratory = Laboratory1.objects.get(pk=pk)
    except Laboratory1.DoesNotExist:
        return Response({'error': 'Laboratory not found'}, status=404)

    serializer = LaboratoryDetailSerializer(laboratory, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_selfstudy(request):
    text = Selfstudy1.objects.all()
    serializer = SelfStudySerializer(text, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trio_images(request):
    images = Trio1.objects.all()
    serializer = TrioSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bilim_images(request):
    images = Bilim1.objects.all()
    serializer = BilimSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_triostudent_images(request):
    images = Trio1.objects.all()
    serializer = TrioStudentSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)

from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_activity_api(request):
    """ Foydalanuvchining haftalik faollik ma'lumotlarini JSON ko'rinishida qaytaradi """
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Dushanba
    days = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"]

    activity_data = {day: 0 for day in days}

    activities = UserActivity.objects.filter(
        user=request.user, date__gte=start_of_week
    )

    for act in activities:
        weekday = act.date.weekday()  # 0=Dush, 6=Yak
        activity_data[days[weekday]] = act.duration

    return Response(activity_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_activity_api(request):
    """ Foydalanuvchi sahifada bo‘lsa, activity vaqtini 1 daqiqa oshiradi """
    today = datetime.today().date()
    activity, _ = UserActivity.objects.get_or_create(user=request.user, date=today)

    time_diff = (now() - activity.updated_at).total_seconds() / 60
    if time_diff >= 1:
        activity.duration += 1
        activity.save()

    return Response({"status": "updated", "new_duration": activity.duration})


from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_user_count_api(request):
    """ Har kuni nechta unikal foydalanuvchi kirganini hisoblaydi """
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Dushanbadan boshlanadi

    user_activity = UserChart.objects.filter(date__gte=start_of_week) \
        .values('date') \
        .annotate(count=Count('user', distinct=True))

    # Kunlar nomi
    days = ["Dush", "Sesh", "Chor", "Pay", "Juma", "Shan", "Yak"]
    result = {day: 0 for day in days}

    for entry in user_activity:
        weekday = entry['date'].weekday()  # 0 = Dushanba, 6 = Yakshanba
        result[days[weekday]] = entry['count']

    return Response({
        "days": list(result.keys()),
        "counts": list(result.values())
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_stars(request):
    """ Foydalanuvchining yulduzlar miqdorini qaytaradi """
    try:
        user_profile = ProfileUser.objects.get(user=request.user)
        return Response({"stars": user_profile.stars})
    except ProfileUser.DoesNotExist:
        return Response({"error": "User profile not found"}, status=404)
  
from django.db.models import Sum  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_stars(request):
    """ Foydalanuvchining bugungi yulduzlar miqdorini qaytaradi """
    today = datetime.today().date()
    today_stars = StarsHistory.objects.filter(user=request.user, date=today).aggregate(Sum('stars'))["stars__sum"] or 0
    return Response({"today_stars": today_stars})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_contact(request):
    images = Admin_Contact.objects.all()
    serializer = AdminContactSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_media_images(request):
    images = Admin_Contact.objects.all()
    serializer = MediaSerializer(images, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_about_us(request):
    """About us sahifasidagi matnni qaytaradi"""
    about_us = about_us_model.objects.first()  # faqat bitta yozuvni olish
    if about_us:
        return Response({"text": about_us.text})
    else:
        return Response({"message": "No content available"}, status=404)
  
  
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_api(request):
    """Foydalanuvchi xabar yuboradi"""
    data = request.data
    try:
        sender_profile = ProfileUser.objects.get(user=request.user)  # Yuboruvchi profilini olish
        receiver_profile = ProfileUser.objects.get(id=data["receiver_id"])  # Qabul qiluvchini olish
        text = data["text"]
        
        # Xabar yaratish
        Message.objects.create(sender=sender_profile, receiver=receiver_profile, text=text)
        
        return Response({"status": "success", "message": "Xabar yuborildi!"})
    
    except KeyError:
        return Response({"error": "Receiver ID yoki text maydoni topilmadi!"}, status=400)
    
    except ProfileUser.DoesNotExist:
        return Response({"error": "Receiver topilmadi!"}, status=404)
    
@api_view(['GET'])
def get_students_api(request):
    """Talabalar ro‘yxatini qaytaradi"""
    students = ProfileUser.objects.filter(role="student").values("id", "full_name", "phone_number")
    return Response({"students": list(students)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications_api(request):
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
    
    return Response({"notifications": notifications})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read_api(request):
    """Bitta xabarni o‘qilgan deb belgilash"""
    data = request.data
    message_id = data.get("message_id")
    
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return Response({"status": "success", "message": "Xabar o‘qildi!"})
    except Message.DoesNotExist:
        return Response({"error": "Xabar topilmadi"}, status=404)
     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_notifications_api(request):
    """O‘qilmagan xabarlar sonini qaytaradi"""
    user_profile = ProfileUser.objects.get(user=request.user)
    unread_count = Message.objects.filter(receiver=user_profile, is_read=False).count()
    return Response({"unread_count": unread_count}) 

@api_view(['GET'])
def get_teachers_api(request):
    """O‘qituvchi ro‘yxatini qaytaradi"""
    teachers = ProfileUser.objects.filter(role="teacher").values("id", "full_name", "phone_number")
    return Response({"teachers": list(teachers)}) 



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # faqat autentifikatsiya qilingan foydalanuvchilar uchun
def create_lesson(request):
    """ O'qituvchi yangi dars yaratadi """
    title = request.data.get("title")
    meet_link = request.data.get("meet_link")  # Google Meet link

    # Yangi darsni yaratish
    lesson = Lesson.objects.create(title=title, meet_link=meet_link)
    return Response({"status": "success", "message": "Dars yaratildi", "lesson_id": lesson.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_lessons(request):
    """ Talabalar uchun mavjud darslar ro'yxatini olish """
    lessons = Lesson.objects.filter(is_active=True)
    lessons_data = [{"id": lesson.id, "title": lesson.title, "meet_link": lesson.meet_link} for lesson in lessons]
    return Response({"lessons": lessons_data})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # faqat autentifikatsiya qilingan o'qituvchilar uchun
def end_stream(request, lesson_id):
    """ Streamni tugatish """
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Stream holatini yangilash
    lesson.is_active = False
    lesson.save()

    return Response({"message": "Stream tugatildi", "lesson_id": lesson.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # faqat autentifikatsiya qilingan foydalanuvchilar uchun
def get_exam_list(request):
    """ Testlar ro'yxatini olish """
    exams = Exam.objects.all()
    exams_data = [{"id": exam.id, "title": exam.title} for exam in exams]
    return Response({"exams": exams_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # faqat autentifikatsiya qilingan foydalanuvchilar uchun
def start_exam(request, exam_id):
    """ Testni boshlash """
    exam = get_object_or_404(Exam, id=exam_id)
    user = request.user

    # Foydalanuvchi uchun test urinishini olish yoki yaratish
    user_attempt, created = UserExamAttempt.objects.get_or_create(user=user, exam=exam)

    if user_attempt.passed:
        return Response({"message": "Testni o'tdingiz!"})

    if user_attempt.attempt_count >= 2:
        return Response({"message": "Testni qayta topshirish imkoniyatingiz qolmadi."}, status=status.HTTP_403_FORBIDDEN)

    if user_attempt.start_time is None or user_attempt.is_time_over():
        user_attempt.start_exam()

    return Response({"message": "Test boshlandi", "exam_id": exam.id})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exam(request, exam_id):
    """ Testni yuborish va natijasini olish """
    exam = get_object_or_404(Exam, id=exam_id)
    user = request.user

    # Foydalanuvchi uchun test urinishini olish
    user_attempt = UserExamAttempt.objects.filter(user=user, exam=exam).first()

    if not user_attempt:
        return Response({"error": "Siz bu testni boshlamadingiz."}, status=status.HTTP_400_BAD_REQUEST)

    questions = ExamQuestion.objects.filter(exam=exam)
    correct_answers = 0
    total_questions = questions.count()

    for question in questions:
        user_answer = request.data.get(f'question_{question.id}')
        if user_answer == question.correct_answer:
            correct_answers += 1

    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    passed = percentage >= 55

    user_attempt.attempt_count += 1
    user_attempt.passed = passed or user_attempt.passed  # Bir marta topsa bo'ldi
    user_attempt.save()

    message = "Tabriklaymiz! Siz testdan o'tdingiz!🎉" if passed else "Afsus, siz testni o'ta olmadingiz."

    return Response({"passed": passed, "percentage": round(percentage, 2), "message": message})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # faqat autentifikatsiya qilingan foydalanuvchilar uchun
def delete_exam(request, exam_id):
    """ Testni o'chirish """
    exam = Exam.objects.filter(id=exam_id, teacher=request.user).first()
    if exam:
        exam.delete()
        return Response({"message": "Test muvaffaqiyatli o'chirildi."})
    return Response({"error": "Test topilmadi yoki sizda bu testni o'chirish huquqi yo'q."}, status=status.HTTP_404_NOT_FOUND)

