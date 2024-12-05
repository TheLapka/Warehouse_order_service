from apps.user_and_email_manager import views
from django.urls import path

urlpatterns = [
    path("warehouse/registration", view=views.RegistrationView.as_view()),
    path("warehouse/user/chekcode", view=views.EmailСonfirmationView.as_view()),
    path("warehouse/reset_password", view=views.SendResetPasswordCodeView.as_view()),
    path(
        "user/me",
        view=views.UserViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
    path("check_code/me", view=views.PasswordResetServiceView.as_view()),
    path("reset/password/me", view=views.ResetPasswordView.as_view()),
]
