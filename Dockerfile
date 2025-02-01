# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только зависимости и requirements.txt
COPY app/requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем остальные файлы проекта
COPY app/ /app/

# Указываем команду для запуска бота
CMD ["python", "bot.py"]