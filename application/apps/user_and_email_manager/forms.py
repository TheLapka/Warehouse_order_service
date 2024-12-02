from apps.user_and_email_manager.models import CustomUser
from django import forms


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "last_login",
            "is_active",
            "is_superuser",
            "is_staff",
            "password",
        )
