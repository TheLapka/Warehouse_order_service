PURPOSE_MAPPING = {
    "verify_email": {
        "subject": "Ваш код подтверждения",
        "template": "user_and_email_manager/reg.html",
        "context": {"code": str},
    },
    "pay_prod": {
        "subject": "Ваш заказ",
        "template": "user_and_email_manager/order.html",
        "context": {"data"},
    },
}


TIME_OUTS = {
    "time_for_confirmation": 172800,
    "time_to_warn": 86400,
    "confirmation_time": 300,
}
