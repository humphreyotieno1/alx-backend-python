# Messaging App

A Django-based messaging application.

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

Run tests with:
```bash
pytest
```

## Code Quality

Run flake8:
```bash
flake8
```

## Docker

Build the Docker image:
```bash
docker build -t messaging-app .
```

Run the container:
```bash
docker run -p 8000:8000 messaging-app
```

## CI/CD

The project uses GitHub Actions for CI/CD. The following workflows are defined:

- `ci.yml`: Runs tests and code quality checks on push and pull requests
- `dep.yml`: Builds and pushes Docker image to Docker Hub on push to main branch
