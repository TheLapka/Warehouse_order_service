from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер модели пользоватея с емейлом в качестве основного авторизационного поля."""

    def create_user(self, email, password, **extra_fields):
        """Создание нового пользователя по емейлу и паролю."""

        if not email:
            raise ValueError(verbose_name="E-mail обязательное поле.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создание супер-пользователя по емейлу и паролю."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # extra_fields.setdefault("user_type", UserType.ADMIN) #Надо узнать почему ни-ни

        if extra_fields.get("is_staff") is not True:
            raise ValueError(verbose_name="Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(verbose_name="Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
