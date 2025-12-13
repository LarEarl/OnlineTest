FROM python:3.11-slim

# Создаём обычного пользователя (НЕ root)
RUN useradd -m runner
USER runner

WORKDIR /app

COPY runner.py /app/runner.py

ENTRYPOINT ["python", "/app/runner.py"]
