# Builder
FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Runtime
FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN python manage.py collectstatic --noinput

RUN useradd -m -u 1000 django \
 && chown -R django:django /app

USER django

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind=0.0.0.0:8000"]
