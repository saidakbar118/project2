from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from main.models import *

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password1']

        user = User.objects.create_user(username=username, password=password)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect username or password.")
        data['user'] = user
        return data


class RoleSelectSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=ProfileUser.ROLE_CHOICES)

    def save(self, **kwargs):
        user = self.context['request'].user
        profile, created = ProfileUser.objects.get_or_create(user=user)
        profile.role = self.validated_data['role']
        profile.save()
        return profile


class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['full_name', 'workplace', 'department', 'phone_number', 'birthdate', 'profile_pic']


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['full_name', 'university', 'faculty', 'specialization', 'grade', 'phone_number', 'birthdate', 'profile_pic']
        

class LectureTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTest
        fields = ['id', 'savol', 'a_javob', 'b_javob', 'c_javob', 'd_javob']       
        

class PracticTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTest
        fields = ['id', 'savol', 'a_javob', 'b_javob', 'c_javob', 'd_javob'] 
        
        
class LaboratoryTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTest
        fields = ['id', 'savol', 'a_javob', 'b_javob', 'c_javob', 'd_javob']  
        
        
class TeacherPage1Serializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherPage1
        fields = '__all__'

class StudentPage1Serializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPage1
        fields = '__all__'  
        
class Profile1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile1
        fields = '__all__' 
        
class ObjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objects1
        fields = '__all__'  
        
        
class LectureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture1
        fields = ['id', 'maruza_raqam', 'maruza_nomi']


class LectureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture1
        fields = ['id', 'maruza_video', 'maruza_raqam', 'maruza_nomi', 'maruza_matni']
        
        
class PracticListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practic1
        fields = ['id', 'practic_raqam', 'practic_nomi']


class PracticDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practic1
        fields = ['id', 'practic_video', 'practic_raqam', 'practic_nomi', 'practic_matni']
        
        
class LaboratoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory1
        fields = ['id', 'laboratory_raqam', 'laboratory_nomi']


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory1
        fields = ['id', 'laboratory_video', 'laboratory_raqam', 'laboratory_nomi', 'laboratory_matni']
        
        
class SelfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selfstudy1
        fields = '__all__'
        
        
class TrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trio1
        fields = ['image1', 'image2', 'image3', 'image4']
        
        
class BilimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bilim1
        fields = '__all__'

        
class TrioStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trio1
        fields = ['image1', 'image2', 'image5', 'image4']
        
        
class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['date', 'duration']
        
        
class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Contact
        fields = ['image1', 'image2', 'image3']
        

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Contact
        fields = ['extra_image', 'image2', 'image3']        