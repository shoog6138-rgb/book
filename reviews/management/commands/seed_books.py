from django.core.management.base import BaseCommand

from reviews.models import Book


class Command(BaseCommand):
    help = 'Insert sample books for local API testing.'

    def handle(self, *args, **options):
        books = [
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'description': 'A practical guide to writing readable, maintainable software.',
            },
            {
                'title': 'Django for APIs',
                'author': 'William S. Vincent',
                'description': 'A focused guide to building APIs with Django and Django REST Framework.',
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt and David Thomas',
                'description': 'A classic book about practical software craftsmanship.',
            },
        ]

        for book in books:
            Book.objects.update_or_create(title=book['title'], defaults=book)

        self.stdout.write(self.style.SUCCESS('Sample books inserted.'))
