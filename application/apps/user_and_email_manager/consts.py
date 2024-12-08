PURPOSE_MAPPING = {
    "verify_email": {
        "subject": "Ваш код для сброса пароля",
        "template": "user_and_email_manager/reset_pass.html",
        "context": {"code": str},
    },
    "pay_prod": {
        "subject": "Ваш заказ",
        "template": "user_and_email_manager/order.html",
        "context": {"data"},
    },
    "activation_warning": {
        "subject": "Время на подтверждение аккаунта заканчивается",
        "template": "user_and_email_manager/order.html",
        "context": {"data"},
    },
    "delete_account": {
        "subject": "Время на подтверждение аккаунта кончилось, аккаунт удалён",
        "template": "user_and_email_manager/order.html",
        "context": {"data"},
    },
    "reg_account": {
        "subject": "Регистрация на складе как пользователь",
        "template": "user_and_email_manager/reg.html",
        "context": {"code": str},
    },
}


TIME_OUTS = {
    "time_for_confirmation": 172800,
    "time_to_warn": 86400,
    "confirmation_time": 300,
}
