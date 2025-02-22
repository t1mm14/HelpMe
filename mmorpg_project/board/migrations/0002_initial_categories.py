from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('board', 'Category')
    categories = [
        'Танки',
        'Хилы',
        'ДД',
        'Торговцы',
        'Гилдмастеры',
        'Квестгиверы',
        'Кузнецы',
        'Кожевники',
        'Зельевары',
        'Мастера заклинаний'
    ]
    for category_name in categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):
    dependencies = [
        ('board', '0001_initial'),  # Укажите предыдущую миграцию
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ] 