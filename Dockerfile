FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 ADD THIS BLOCK (CRITICAL FIX)
RUN mkdir -p /usr/local/lib/python3.11/site-packages/openenv
RUN echo "__version__ = '0.2.0'" > /usr/local/lib/python3.11/site-packages/openenv/__init__.py

COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]