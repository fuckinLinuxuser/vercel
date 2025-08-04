FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

RUN pip  install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Команда запуска бота
CMD ["python", "main.py"]
