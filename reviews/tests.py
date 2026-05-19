from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book, Review


class BookReviewApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reader', password='StrongPass123!')
        self.other_user = User.objects.create_user(username='otherreader', password='StrongPass123!')
        self.admin = User.objects.create_superuser(username='admin', password='AdminPass123!')
        self.book = Book.objects.create(
            title='Django for APIs',
            author='William S. Vincent',
            description='A practical API book.',
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newreader',
                'email': 'newreader@example.com',
                'password': 'NewStrongPass123!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newreader').exists())

    def test_user_can_obtain_jwt_token(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'reader', 'password': 'StrongPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_public_can_browse_books(self):
        response = self.client.get(reverse('book_list_create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.book.title)

    def test_only_admin_can_create_books(self):
        response = self.client.post(
            reverse('book_list_create'),
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'description': 'A software craftsmanship book.',
            },
            format='json',
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('book_list_create'),
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'description': 'A software craftsmanship book.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title='Clean Code').exists())

    def test_authenticated_user_can_review_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('book_reviews', args=[self.book.id]),
            {'rating': 5, 'comment': 'Excellent book for API developers.'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.user)

    def test_only_review_owner_can_edit_or_delete_review(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=4,
            comment='Helpful and concise.',
        )

        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(
            reverse('review_detail', args=[review.id]),
            {'rating': 1, 'comment': 'Trying to edit another user review.'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse('review_detail', args=[review.id]),
            {'rating': 5, 'comment': 'Updated by the owner.'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)

    def test_authenticated_user_can_change_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('change_password'),
            {'old_password': 'StrongPass123!', 'new_password': 'BetterPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BetterPass123!'))
