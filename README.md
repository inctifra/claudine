# Django Starter Template

License: Apache Software License 2.0

---

## 🚀 Quick Start

Once you have cloned the repository, you can set up and run both the backend (Django) and frontend (Webpack + pnpm) with the following simple steps.

### 1. Sync Python environment

```bash
uv sync
```

### 2. Install frontend dependencies

```bash
pnpm install
```

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Run development servers

* Start the **frontend** development server:

  ```bash
  pnpm dev
  ```

* In another terminal, start the **Django backend**:

  ```bash
  python manage.py runserver
  ```

### 5. Production build

To build frontend assets for production:

```bash
pnpm build
```

---

## ⚙️ Settings

See [Cookiecutter Django Settings Documentation](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html)

---

## 🗄️ Django Cache Configuration

This project supports both:

* **Redis cache** (recommended for production)
* **Database cache fallback** (useful for offline/local environments)

### Cache Configuration

```python
# CACHES
# ------------------------------------------------------------------------------

BACKEND_CACHE_DB_AVAILABLE = env.bool("BACKEND_CACHE_DB_AVAILABLE", default=True)

DB_CACHE_ALIASES = {
    "default": "default",
    "offline": "offline_cache",
}

_OFFLINE_CACHE_BACKEND = {
    "BACKEND": "django.core.cache.backends.db.DatabaseCache",
    "LOCATION": DB_CACHE_ALIASES["offline"],
}

_ONLINE_CACHE_BACKEND = {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": REDIS_URL,
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        "IGNORE_EXCEPTIONS": True,
    },
}

CACHES = {
    "default": _ONLINE_CACHE_BACKEND
    if BACKEND_CACHE_DB_AVAILABLE
    else _OFFLINE_CACHE_BACKEND,
}
```

### Creating the Django Cache Table

If you are using the database cache backend, create the cache table with:

```bash
python manage.py createcachetable offline_cache
```

You can verify the table was created successfully by running:

```bash
python manage.py showmigrations
```

or directly inspecting your database tables.

### Environment Variables

Example `.env` configuration:

```env
BACKEND_CACHE_DB_AVAILABLE=True
REDIS_URL=redis://127.0.0.1:6379/1
```

### Notes

* When `BACKEND_CACHE_DB_AVAILABLE=True`, Redis will be used.
* When set to `False`, Django automatically falls back to the database cache table.
* The database cache backend is useful during local development when Redis is unavailable.

---

## 👥 User Setup

### Create a Normal User

Register through the Sign Up page and check your console for the email verification link.

### Create a Superuser

```bash
python manage.py createsuperuser
```

---

## ✅ Type Checks

Run static type checks using **mypy**:

```bash
mypy claudine
```

---

## 🧪 Testing

Run all tests and generate a coverage report:

```bash
coverage run -m pytest
coverage html
```

Open the coverage report:

```bash
open htmlcov/index.html
```

or simply run:

```bash
pytest
```

---

## 🔄 Celery Setup

### Run Celery Worker

```bash
cd claudine
celery -A config.celery_app worker -l info
```

### Run Celery Beat

```bash
cd claudine
celery -A config.celery_app beat
```

### Run Worker + Beat Together (Local Development Only)

```bash
celery -A config.celery_app worker -B -l info
```

---

## 📧 Email Server (Development)

Local SMTP server Mailpit is preconfigured via Docker.

Access the Mailpit UI at:

```text
http://127.0.0.1:8025
```

Official project:

[Mailpit GitHub Repository](https://github.com/axllent/mailpit)

---

## Error Logging (Sentry)

To enable Sentry, set the DSN URL in your production environment variables.

Official website:

[Sentry](https://sentry.io)

---

## 🚢 Deployment Options

### Heroku

Refer to the deployment guide:

[Cookiecutter Django Heroku Deployment Guide](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-on-heroku.html)

### Docker

Refer to the deployment guide:

[Cookiecutter Django Docker Deployment Guide](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html)

---

## 🎨 Custom Bootstrap Compilation

You can customize Bootstrap by editing variables in:

```text
static/sass/custom_bootstrap_vars
```

CSS will automatically rebuild via Webpack when running:

```bash
pnpm dev
```

or:

```bash
pnpm build
```
