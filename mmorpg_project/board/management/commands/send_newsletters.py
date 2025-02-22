from django.core.management.base import BaseCommand
from board.models import Newsletter
from board.tasks import send_newsletter

class Command(BaseCommand):
    help = 'Отправка новостных рассылок'

    def handle(self, *args, **options):
        newsletters = Newsletter.objects.filter(sent_at__isnull=True)
        for newsletter in newsletters:
            send_newsletter(newsletter)
            self.stdout.write(self.style.SUCCESS(f'Рассылка "{newsletter.title}" отправлена')) 