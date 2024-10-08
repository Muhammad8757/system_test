from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from .serializers import ActionDetailSerializer, ActivateWithTestSerializer, TestWithDetailsSerializer, UserLoginSerializer, SubjectDetailSerializer, ThemeDetailSerializer, ActivateCreateSerializer
from .models import Action, User, Subject, Theme, Test, Activate
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
@extend_schema(tags=['User'])
class UserAPIView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data.data)

@extend_schema(tags=['Subjects'])
class SubjectAPIView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubjectDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Subject.objects.filter(user_id=self.request.user)
    
@extend_schema(tags=['Theme'])
class ThemeAPIView(GenericViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['user_id'] = request.user
        subject = serializer.save()
        return Response(self.get_serializer(subject).data, status=201)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"success"}, status=status.HTTP_204_NO_CONTENT)
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@extend_schema(tags=['Tests'])
class TestAPIView(GenericViewSet):
    serializer_class = TestWithDetailsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Test.objects.filter(user_id=self.request.user)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['user_id'] = request.user
        return Response({'success'}, status=201)
    
    def update(self, request, *args, **kwargs):
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
    serializer_class = ActivateCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        return Response(self.get_serializer(subject).data, status=201)
    
    @action(detail=False, methods=['get'])
    def get_activated_tests(self, request):
        activated_tests = Activate.objects.filter(action__id_student=request.user)
        serializer = ActivateWithTestSerializer(activated_tests, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Action'])
class ActionAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionDetailSerializer