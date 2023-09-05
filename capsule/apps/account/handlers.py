from django.conf.global_settings import EMAIL_HOST_USER
from django.utils.translation import gettext as _
from django.template.loader import get_template
from django.core.mail import EmailMessage

from threading import Thread
from random import randint


# Async thread for sending email
class SendEmailThread(Thread):
    def __init__(self, receiver=None, subject=None, message=None):
        super().__init__()
        self.receiver = receiver
        self.subject = subject
        self.message = message

    def run(self) -> None:
        """ Send email via django EmailMessage class """
        email = EmailMessage(subject=self.subject, body=self.message, from_email=EMAIL_HOST_USER, to=[self.receiver])
        email.content_subtype = "html"
        email.send()


# Create email message class
class CreateEmailMessage:
    def __init__(self, verification=False):
        self.subject = None
        self.message = None
        if verification:
            self.code = self.get_random_code()

    def welcome_message(self, link: str) -> tuple[str, str]:
        """ Create and return a welcome message for given name. Returns a tuple like (subject, message),
        or you can access them from created instance: self.subject, self.message """

        self.subject = _("Welcome to Capsule :)")
        self.message = get_template("emails/welcome_email.html").render({"link", link})

        return self.subject, self.message

    def password_reset_message(self, link: str) -> tuple[str, str]:
        """ Create and return a password reset request message. Returns a tuple like (subject, message),
        or you can access them from created instance: self.subject, self.message """

        self.subject = _("Reset user password")
        self.message = get_template("emails/password_reset_email.html").render({"link": link})

        return self.subject, self.message

    def email_verify_message(self) -> tuple[str, str]:
        """ Create and return an email verification message. Returns a tuple like (subject, message),
         or you can access them from created instance: self.subject, self.message """

        self.subject = _("Email verification code")
        self.message = get_template("emails/verification_email.html").render({"code": self.code})

        return self.subject, self.message

    def get_random_code(self) -> str:
        """ Return a 5 digits random string """
        return str(randint(10000, 99999))
