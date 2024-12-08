from apps.user_and_email_manager.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet


class UserRepository:
    def create_user_rep(self, data: dict, password) -> CustomUser:
        user = CustomUser.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            surname=data["surname"],
            email=data["email"],
            password=make_password(password),
        )
        return user

    def get_user_by_email(self, email: str) -> QuerySet[CustomUser]:
        return CustomUser.objects.filter(email=email)
