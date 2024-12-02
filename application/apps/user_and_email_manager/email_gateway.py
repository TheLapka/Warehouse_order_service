from os import environ

from apps.user_and_email_manager.consts import PURPOSE_MAPPING
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class EmailManager:
    """
    Based on received purpose(str) decides
    which templated and context to use
    """

    def __init__(self, purpose: str, **context_data) -> None:
        self.mapping_data = PURPOSE_MAPPING[purpose]
        self.context = context_data

    def get_subject(self) -> str:
        return self.mapping_data["subject"]

    def get_template(self) -> str:
        return self.mapping_data["template"]

    def get_context(self) -> dict:
        return {key: self.context[key] for key in self.mapping_data["context"]}


class EmailGateway:
    def send_email(self, purpose: str, email: str, **context_data):
        manager = EmailManager(purpose=purpose, **context_data)

        send_information_email(
            subject=manager.get_subject(),
            template_name=manager.get_template(),
            to_email=email,
            context=manager.get_context(),
        )


def send_information_email(
    subject: str,
    template_name: str,
    context: dict,
    to_email: list[str] | str,
    **kwargs,
):
    """
    :param subject: email subject
    :param template_name: template path to email template
    :param context: data what will be passed into email
    :param to_email: receiver email(s)
    :param letter_language: translate letter to selected lang
    :param kwargs: from_email, bcc, cc, reply_to and file_path params
    """
    to_email: list = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(
        subject=subject,
        from_email=kwargs.get("from_email"),
        to=to_email,
        bcc=kwargs.get("bcc"),
        cc=kwargs.get("cc"),
        reply_to=kwargs.get("reply_to"),
    )
    html_email: str = loader.render_to_string(template_name, context)
    email_message.attach_alternative(html_email, "text/html")
    if file_path := kwargs.get("file_path"):
        file_path = environ.get("APP_HOME", environ.get("HOME")) + file_path
        email_message.attach_file(file_path, kwargs.get("mimetype"))
    # try:
    return email_message.send()
    # except Exception:
    #     # TODO: Логгирование и обработка ошибки отправки
    #     pass
