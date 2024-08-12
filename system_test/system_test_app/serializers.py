from rest_framework import serializers
from .models import Action, Subject, Theme, Test, Answer, Activate, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        password = attrs['password']
        user = User.objects.get(phone_number = phone_number, password=password)
        if not user:
            raise Exception("user not found")
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    
class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name', 'user_id']

class ThemeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name', 'subject_id']
    
    def create(self, validated_data):
        theme = Theme.objects.create(**validated_data)
        theme.save()
        return theme

class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer']

class TestCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    answers = serializers.ListField()
    correct_answer = serializers.IntegerField()
    
    def create(self, validated_data):
        test = Test.objects.create(
            title=validated_data['title'],
            user_id=self.context['request'].user
        )
        answers_data = validated_data.get('answers', [])
        correct_answer_index = validated_data.get('correct_answer', -1)
        
        for idx, answer_text in enumerate(answers_data):
            Answer.objects.create(
                tests_id=test,
                answer=answer_text,
                is_true=(idx == correct_answer_index)
            )
        return test

class TestWithDetailsSerializer(serializers.Serializer):
    theme_id = serializers.IntegerField()
    test = TestCreateSerializer()

    def create(self, validated_data):
        theme_id = validated_data.get('theme_id')
        test_data = validated_data.get('test')
        user = self.context['request'].user
        
        theme = Theme.objects.get(id=theme_id)

        test = Test.objects.create(
            theme_id=theme,
            title=test_data['title'],
            user_id=user
        )
        
        answers_data = test_data.get('answers', [])
        correct_answer_index = test_data.get('correct_answer', -1)
        
        for idx, answer_text in enumerate(answers_data):
            Answer.objects.create(
                tests_id=test,
                answer=answer_text,
                is_true=(idx == correct_answer_index)
            )
        return test

class TestDetailSerializer(serializers.ModelSerializer):
    answers = AnswerDetailSerializer(many=True, source='answers_set')
    class Meta:
        model = Test
        fields = '__all__'

class ActivateWithTestSerializer(serializers.ModelSerializer):
    id_test = TestDetailSerializer()

    class Meta:
        model = Activate
        fields = ['id_test', 'date_start', 'date_end']

class ActivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activate
        fields = ['id_test', 'date_start', 'date_end']
    
    def create(self, validated_data):
        activate = Activate.objects.create(**validated_data)
        activate.save()
        return activate

class ActiveTestDetailSerializer(serializers.Serializer):
    id_test = TestCreateSerializer()
    class Meta:
        model = Activate
        fields = ['id_test', 'date_start', 'date_end']

class ActionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id_student', 'id_activated']