# Book Review API

A RESTful API for a book review system built with Django REST Framework and JWT authentication.

## Features

- User registration
- JWT login and token refresh
- Password change for authenticated users
- Public book list and book detail endpoints
- Admin-only book create, update, and delete
- Authenticated review creation
- Review editing and deletion restricted to the review owner

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_books
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Base URL:

```text
http://127.0.0.1:8000/api/
```

## Authentication

The API uses JWT authentication from `djangorestframework-simplejwt`.

Log in with:

```http
POST /api/token/
```

Example body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Use the access token in protected requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Refresh the token with:

```http
POST /api/token/refresh/
```

## Endpoints

| Method | URL | Permission | Description |
| --- | --- | --- | --- |
| POST | `/api/register/` | Public | Register a new user |
| POST | `/api/token/` | Public | Obtain JWT access and refresh tokens |
| POST | `/api/token/refresh/` | Public | Refresh JWT access token |
| POST | `/api/change-password/` | Authenticated | Change current user's password |
| GET | `/api/books/` | Public | List all books |
| GET | `/api/books/<id>/` | Public | Retrieve one book |
| POST | `/api/books/` | Admin only | Add a book |
| PUT | `/api/books/<id>/` | Admin only | Edit a book |
| DELETE | `/api/books/<id>/` | Admin only | Delete a book |
| GET | `/api/books/<book_id>/reviews/` | Public | List reviews for one book |
| POST | `/api/books/<book_id>/reviews/` | Authenticated | Add a review to one book |
| PUT | `/api/reviews/<id>/` | Review owner only | Edit a review |
| DELETE | `/api/reviews/<id>/` | Review owner only | Delete a review |

## curl Examples

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d "{\"username\":\"reader\",\"email\":\"reader@example.com\",\"password\":\"StrongPass123!\"}"
```

Get JWT:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"reader\",\"password\":\"StrongPass123!\"}"
```

List books:

```bash
curl http://127.0.0.1:8000/api/books/
```

Add a review:

```bash
curl -X POST http://127.0.0.1:8000/api/books/1/reviews/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{\"rating\":5,\"comment\":\"Excellent book.\"}"
```

Change password:

```bash
curl -X POST http://127.0.0.1:8000/api/change-password/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d "{\"old_password\":\"StrongPass123!\",\"new_password\":\"BetterPass123!\"}"
```

## Tests

```powershell
.\.venv\Scripts\python.exe manage.py test
```
