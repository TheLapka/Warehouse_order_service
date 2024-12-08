from datetime import date, timedelta

from email_gateway import EmailGateway
from warehouse_order_service.celery import app

from .models import CustomUser


@app.task
def send_warning_letter():
    unconfirmed_users = CustomUser.objects.filter(
        is_confired=False,
        date_joined__date__gte=date.today() - timedelta(days=1),
        date_joined__date__lte=date.today() - timedelta(days=2),
    )
    for user in unconfirmed_users:
        EmailGateway().send_email(
            purpose="activation_warning",
            email=user.email,
        )


@app.task
def send_and_del_user():
    unconfirmed_users = CustomUser.objects.filter(
        is_confired=False,
        date_joined__date__lte=date.today() - timedelta(days=2),
    )
    for user in unconfirmed_users:
        EmailGateway().send_email(
            purpose="delete_account",
            email=user.email,
        )
        user.delete()
