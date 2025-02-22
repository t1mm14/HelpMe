from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from board.models import NewsletterSubscription

def send_response_notification(response):
    subject = f'Новый отклик на ваше объявление "{response.advertisement.title}"'
    html_content = render_to_string(
        'board/email/response_notification.html',
        {
            'response': response,
            'advertisement': response.advertisement,
        }
    )
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.advertisement.author.email],
    )

def send_acceptance_notification(response):
    subject = f'Ваш отклик был принят!'
    html_content = render_to_string(
        'board/email/acceptance_notification.html',
        {
            'response': response,
            'advertisement': response.advertisement,
        }
    )
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email],
    )

def send_newsletter(newsletter):
    subscribers = NewsletterSubscription.objects.filter(is_active=True)
    for subscription in subscribers:
        send_mail(
            subject=newsletter.title,
            message='',
            html_message=newsletter.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
        )
    newsletter.sent_at = timezone.now()
    newsletter.save() 