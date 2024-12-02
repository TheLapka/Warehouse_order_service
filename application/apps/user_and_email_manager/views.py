from apps.user_and_email_manager.models import CustomUser
from apps.user_and_email_manager.serializers import (
    CheckRestPasswordCodeSerializer,
    ProfileModelSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
    SendResetPasswordCodeSerializer,
)
from apps.user_and_email_manager.services import (
    PasswordResetService,
    RegistrationCreate,
    SendResetPasswordEmail,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return CustomUser.objects.none()

    def post(self, request):
        sz = RegistrationSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        creator = RegistrationCreate()
        creator.create_user(sz.data)
        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileModelSerializer

    def get_object(self):
        return self.request.user


class SendResetPasswordCodeView(GenericAPIView):
    serializer_class = SendResetPasswordCodeSerializer

    def get_queryset(self):
        return CustomUser.objects.none()

    def post(self, request):
        sz = SendResetPasswordCodeSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        send_email = SendResetPasswordEmail()
        send_email.send_reset_pass(sz.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetServiceView(GenericAPIView):
    serializer_class = CheckRestPasswordCodeSerializer

    def get_queryset(self):
        return CustomUser.objects.none()

    def post(self, request):
        sz = CheckRestPasswordCodeSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        checker = PasswordResetService()
        key = checker.check_reset_pass_code(sz.data["email"], sz.data["code"])
        return Response(data={"key": key}, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        sz = ResetPasswordSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        reset_pass = PasswordResetService()
        reset_pass.reset_password(sz.data["key"], sz.data["password_1"])
        return Response(status=status.HTTP_200_OK)
