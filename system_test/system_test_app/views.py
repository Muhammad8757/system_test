from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from .serializers import FullTestSerializer, ListAnswersSerializer, LoginSerializer, UserSerializer, SubjectSerializer, ThemeSerializer, TestSerializer, AnswerSerializer, ActivateSerializer
from .models import User, Subjects, Theme, Tests, Answers, Activate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
@extend_schema(tags=['User'])
class UserAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(phone_number=phone_number, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                return Response({"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Subjects'])
class SubjectAPIView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Subjects.objects.filter(user_id=self.request.user)
    
@extend_schema(tags=['Theme'])
class ThemeAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['user_id'] = request.user
        subject = serializer.save()
        return Response(self.get_serializer(subject).data, status=201)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        instance = self.get_object()
        if request.user == instance.user:
            instance.delete()
            return Response({"success"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "you have not a rights"}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@extend_schema(tags=['Tests'])
class TestAPIView(GenericViewSet):
    serializer_class = FullTestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Tests.objects.filter(user_id=self.request.user)
    
    def create(self, request):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['user_id'] = request.user
        subject = serializer.save()
        return Response(self.get_serializer(subject).data, status=201)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            instance.delete()
            return Response({"success"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "you have not a rights"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Activate'])
class ActivateAPIView(GenericViewSet):
    queryset = Activate.objects.all()
    serializer_class = ActivateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        if not request.user.is_teacher:
            raise Exception("you have not a rights")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        return Response(self.get_serializer(subject).data, status=201)