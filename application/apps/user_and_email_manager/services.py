import random
from uuid import UUID, uuid4

from apps.user_and_email_manager.consts import TIME_OUTS
from apps.user_and_email_manager.email_gateway import EmailGateway
from apps.user_and_email_manager.repository import UserRepository
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.db import DatabaseError, transaction
from rest_framework.serializers import ValidationError


class SendVerificationCode:
    def generate_and_send_code_according_to_condition(
        self, email: str, timeout: int
    ) -> None:
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(email, value=code, timeout=timeout)

        EmailGateway().send_email(
            purpose="reg_account",
            email=email,
            code=code,
        )


class RegistrationCreate:
    def create_user(self, data: dict) -> None:
        rep = UserRepository()
        user = rep.get_user_by_email(email=data["email"])
        user = user.first()
        if user is None:
            if data["password_1"] != data["password_2"]:
                raise ValidationError(detail="Пароли должны совпадать")
            password = data["password_1"]
            try:
                with transaction.atomic():
                    user = rep.create_user_rep(data, password)
            except DatabaseError as e:
                raise ValidationError(
                    detail=f"Произошла ошибка при создании данных: {str(e)}"
                )

            SendVerificationCode().generate_and_send_code_according_to_condition(
                email=user.email, timeout=TIME_OUTS["time_for_confirmation"]
            )
        else:
            raise ValidationError(detail="Email уже используется")


class EmailConfirmationService:
    def email_cofirm(self, email: str, code: str) -> None:
        rep = UserRepository()
        codes = cache.get(email) == code
        if codes:
            cache.delete(email)
            user = rep.get_user_by_email(email=email)
            try:
                with transaction.atomic():
                    user.update(is_confired=True)
            except DatabaseError as e:
                raise ValidationError(
                    detail=f"Произошла ошибка при обновлении данных: {str(e)}"
                )
        else:
            raise ValidationError(
                {"detail": "Проверка не пройдена, заново запросите код."}
            )


class SendResetPasswordEmail:
    def send_reset_pass(self, data: dict) -> None:
        rep = UserRepository()
        user = rep.get_user_by_email(email=data["email"])
        user = user.first()
        if user is None:
            raise ValidationError(
                {"detail": "Пользователя с таким Email не существует."}
            )

        SendVerificationCode().generate_and_send_code_according_to_condition(
            email=user.email, timeout=TIME_OUTS["confirmation_time"]
        )


class PasswordResetService:
    def check_reset_pass_code(self, email: str, code: str) -> UUID:
        status = cache.get(email) == code
        if status:
            key = uuid4()
            cache.set(f"{key}-passed", value=email, timeout=300)
            return key
        raise ValidationError({"detail": "Неверный код"})

    def reset_password(self, key: UUID, password: str) -> None:
        rep = UserRepository()
        email = cache.get(f"{key}-passed")
        if not email:
            raise ValidationError(
                {"detail": "Проверка не пройдена, заново запросите код."}
            )

        user = rep.get_user_by_email(email=email)
        cache.delete(f"{key}-passed")
        try:
            with transaction.atomic():
                user.update(password=make_password(password))
        except DatabaseError as e:
            raise ValidationError(
                detail=f"Произошла ошибка при обновлении данных: {str(e)}"
            )
