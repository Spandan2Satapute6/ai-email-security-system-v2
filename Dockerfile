FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# 🔥 upgrade pip safely
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 🔥 install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]