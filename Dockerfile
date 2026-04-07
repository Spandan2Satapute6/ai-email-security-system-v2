FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 CREATE FAKE PACKAGE (IMPORTANT)
RUN mkdir openenv_pkg && \
    echo "from setuptools import setup\nsetup(name='openenv', version='0.2.0')" > openenv_pkg/setup.py && \
    pip install ./openenv_pkg

COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]