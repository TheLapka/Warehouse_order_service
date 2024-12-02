import random
from uuid import UUID, uuid4

from apps.user_and_email_manager.consts import TIME_OUTS
from apps.user_and_email_manager.email_gateway import EmailGateway
from apps.user_and_email_manager.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.serializers import ValidationError


class SendVerificationCode:
    def generate_and_send_code_according_to_condition(
        self, email: str, timeout: int
    ) -> None:
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(email, value=code, timeout=timeout)

        EmailGateway().send_email(
            purpose="verify_email",
            email=email,
            code=code,
        )


class RegistrationCreate:
    def create_user(self, data):
        users = CustomUser.objects.filter(email=data["email"]).first()
        if users is None:
            if data["password_1"] != data["password_2"]:
                raise ValidationError(detail="Пароли должны совпадать")
            password = data["password_1"]
            user = CustomUser.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                surname=data["surname"],
                email=data["email"],
                password=make_password(password),
            )

            SendVerificationCode().generate_and_send_code_according_to_condition(
                email=user.email, timeout=TIME_OUTS["time_for_confirmation"]
            )
        else:
            raise ValidationError(detail="Email уже используется")


class SendResetPasswordEmail:
    def send_reset_pass(self, data):
        user = CustomUser.objects.filter(email=data["email"]).first()
        if user is None:
            raise ValidationError(
                {"detail": "Пользователя с таким Email не существует."}
            )

        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(user.email, value=code, timeout=300)

        EmailGateway().send_email(
            purpose="verify_email",
            email=user.email,
            code=code,
        )


class PasswordResetService:
    def check_reset_pass_code(self, email: str, code: str) -> UUID:
        status = cache.get(email) == code
        if status:
            key = uuid4()
            cache.set(f"{key}-passed", value=email, timeout=300)
            return key
        raise ValidationError({"detail": "Неверный код"})

    def reset_password(self, key: UUID, password: str):
        email = cache.get(f"{key}-passed")
        if not email:
            raise ValidationError(
                {"detail": "Проверка не пройдена, заново запросите код."}
            )

        user = CustomUser.objects.filter(email=email)
        cache.delete(f"{key}-passed")
        user.update(password=make_password(password))

        # Сделать подтверждение регистрации, авторизация jwt token
