from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.db import transaction
from .models import User, ActivationCode


@receiver(post_save, sender=User)
def check_registration(sender, instance, created, **kwargs):
    if created:
        obj, raw_code = ActivationCode.create_for_user(instance)

        def _after_commit_send():
            subject = 'Код подтверждения регистрации'
            message = f'Привет, {instance.username}!\n\nВаш код подтверждения: {raw_code}\n\n Действителен 15 минут \n\n Если вы не регестрировались - проигнорируете это письмо \n\n Спасибо за регистрацию!'

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[instance.email]
                )
            except Exception:
                pass

        transaction.on_commit(_after_commit_send)
