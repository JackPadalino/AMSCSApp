from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import SchoolYear,Classroom,ProjectTopic,Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username', 'email', 'groups']

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ['id','year']

class ClassroomSerializer(serializers.ModelSerializer):
    school_year = SchoolYearSerializer()
    class Meta:
        model = Classroom
        fields = ['id','title', 'join_code','school_year']

class ProjectTopicSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer()
    class Meta:
        model = ProjectTopic
        fields = ['id','title','classroom']

class ProjectSerializer(serializers.ModelSerializer):
    project_topic = ProjectTopicSerializer()
    user = UserSerializer()
    class Meta:
        model = Project
        fields = ['id','title', 'description','project_link','date_posted','project_topic','user']