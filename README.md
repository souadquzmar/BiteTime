# Django Project Skeleton

A reusable Django REST Framework project skeleton.

## Requirements

* Python 3.14+
* [uv](https://docs.astral.sh/uv/)
* PostgreSQL

## Setup

### 1. Clone the repository

```bash
git clone <TEMPLATE_REPOSITORY_URL> <PROJECT_NAME>
cd <PROJECT_NAME>
```

### 2. Create a new Git repository

Remove the existing Git metadata from the template:

```bash
rm -rf .git
```

Initialize a new repository:

```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. Set up the virtual environment

Create and activate the virtual environment:

```bash
uv venv
source .venv/bin/activate
```

Install the dependencies:

```bash
uv sync
```

### 4. Configure environment variables

Create the `.env` file from the provided example:

```bash
cp .env.example .env
```

Update the `.env` file with your local configuration:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your-database-url
```

### 5. Rename the project package

Rename the root Django project package to the name of your new project.

Update references to the old package name in:

* `settings.py`
* `urls.py`
* `asgi.py`
* `wsgi.py`

### 6. Run migrations

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## Run

Start the development server:

```bash
uv run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/api/schema/swagger-ui/
```

ReDoc:

```text
http://127.0.0.1:8000/api/schema/redoc/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```
