FROM python:3.10

LABEL authors="kozak_mamay"

# Встановимо робочу директорію
WORKDIR /app

# Спочатку копіюємо requirements.txt для кращого кешування шарів
COPY requirements.txt .

# Встановимо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код додатку
COPY . .

# Позначимо порт, де працює застосунок
EXPOSE 8000

# Запустимо FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]