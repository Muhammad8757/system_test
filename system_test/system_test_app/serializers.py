from rest_framework import serializers
from .models import User, Subjects, Theme, Tests, Answers, Activate


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'password']

    def validate(self, data):
        if len(str(data.get('phone_number', ''))) < 9:
            raise Exception("enter more than 9 characters ")
        return data

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['id','name', 'user_id']

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['name', 'subject_id']
    
    def create(self, validated_data):
        theme = Theme.objects.create(**validated_data)
        theme.save()
        return theme

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['answer']

class TestSerializer(serializers.Serializer):
    title = serializers.CharField()
    answers = serializers.ListField()
    correct_answer = serializers.IntegerField()
    
    def create(self, validated_data):
        test = Tests.objects.create(**validated_data)
        test.save()
        return test


class FullTestSerializer(serializers.Serializer):
    theme_id = serializers.IntegerField()
    test = TestSerializer()

    def create(self, validated_data):
        theme_id = validated_data.get('theme_id')
        title = validated_data.get('title')
        user = validated_data.get('user_id')
        test = Tests.objects.create(theme_id, title, user)
        test.save()
        return test


class ListAnswersSerializer(serializers.Serializer):
    tests_id = serializers.IntegerField()

class ActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activate
        fields = ['id_test', 'date_start', 'date_end']