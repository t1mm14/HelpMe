from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Advertisement, Response, NewsletterSubscription
from django.conf import settings

@receiver(post_save, sender=Advertisement)
def notify_subscribers_new_advertisement(sender, instance, created, **kwargs):
    if created:  # Только для новых объявлений
        subscribers = NewsletterSubscription.objects.filter(is_active=True)
        
        for subscription in subscribers:
            context = {
                'username': subscription.user.username,
                'title': instance.title,
                'content': instance.content[:200] + '...' if len(instance.content) > 200 else instance.content,
                'category': instance.category.name,
            }
            
            html_message = render_to_string('email/new_advertisement.html', context)
            
            send_mail(
                subject=f'Новое объявление в категории {instance.category.name}',
                message=f'Появилось новое объявление: {instance.title}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
                html_message=html_message,
            )

@receiver(post_save, sender=Response)
def notify_author_new_response(sender, instance, created, **kwargs):
    if created:  # Только для новых откликов
        advertisement = instance.advertisement
        
        context = {
            'username': advertisement.author.username,
            'advertisement_title': advertisement.title,
            'response_author': instance.author.username,
            'response_text': instance.text,
        }
        
        html_message = render_to_string('email/new_response.html', context)
        
        send_mail(
            subject=f'Новый отклик на ваше объявление "{advertisement.title}"',
            message=f'Пользователь {instance.author.username} оставил отклик на ваше объявление',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[advertisement.author.email],
            html_message=html_message,
        ) 