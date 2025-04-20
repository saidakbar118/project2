from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/',auth_view),
    path('choice/',role_selection_view,name='role_selection'),
    path('teacherregister/',teacher_profile_update_view),
    path('studentregister/',student_profile_update_view),
    path('send-code/', request_password_reset_view, name='send-code'),
    path('verify-code/', verify_code_view, name='verify-code'),
    path('reset-password/', reset_password_view, name='reset-password'),
    path('entrance/',Entrance),
    path('success/',Success),
    path('teacherpage/',TeacherPage),
    path('studentpage/',StudentPage),
    path('profile/',Profile),
    path('teacher_profile-fix/',TeacherProfileFix),
    path('student_profile-fix/',StudentProfileFix),
    path('objects/',Objects),
    path('objects/lecture/',Lecture),
    path('lecturedetail/<int:pk>/',LectureDetail.as_view()),
    path('objects/practic/',Practic),
    path('practicdetail/<int:pk>/',PracticDetail.as_view()),
    path('objects/laboratory/',Laboratory),
    path('laboratorydetail/<int:pk>/',LaboratoryDetail.as_view()),
    path('objects/selfstudy/',Selfstudy),
    path('trio/',Trio),
    path('triostudent/',TrioStudent),
    path('bilim/',Bilim),
    path('stars/',Stars, name="stars"),
    path('starsdaily/',StarsDaily, name="stars-daily"),
    path('home/',Home), 
    path('admincontact/',AdminContact),
    path('lecture-test/<int:lesson_id>/', TestForLecture, name='test_for_lecture'),
    path('practic-test/<int:lesson_id>/', TestForPractic, name='test_for_practic'),
    path('laboratory-test/<int:lesson_id>/', TestForLaboratory, name='test_for_laboratory'),
    path("activity/", activity_page, name="activity_page"),
    path("activity/data/", get_activity_data, name="get_activity_data"),
    path("activity/log/", log_activity, name="log_activity"),
    path("chart/", Chart, name="chart"),
    path("chart/data/", weekly_user_count, name="weekly-user-count"),
    path("aboutus/",AboutUs),
    path("trio/suniy/",suniy_intelekt),
    path("triostudent/suniy/",suniy_intelekt),
    path("media/",media_view),
    path("studentcontact/", StudentContact, name="studentcontact"),  # Sahifa ochish
    path("send_message/", send_message, name="send_message"),  # Xabar yuborish API
    path("get_students/", get_students, name="get_students"),
    path("notifications/", Notifications, name="notifications_page"),  # Sahifani ko‘rsatadi
    path("get_notifications/", get_notifications, name="get_notifications"),
    path("teachercontact/", TeacherContact, name="teacher_contact"),
    path("send_teacher_message/", send_teacher_message, name="send_teacher_message"),
    path("get_teachers/", get_teachers, name="get_teachers"),
    path("get_unread_notifications/", get_unread_notifications, name="get_unread_notifications"),
    path("mark_notifications_as_read/", mark_notification_as_read, name="mark_notifications_as_read"),
    path("teacher/", teacher_page, name="teacher_page"),
    path("student/", student_page, name="student_page"),
    path("end_stream/<int:lesson_id>/", end_stream, name="end_stream"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('bilim/exam/',start_exam, name="start_exam"),
]

if settings.DEBUG:  # Faqat local server uchun
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)