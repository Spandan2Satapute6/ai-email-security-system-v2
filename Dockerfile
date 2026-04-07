FROM python:3.11-slim

WORKDIR /app

# 🔥 Copy pyproject + lock file FIRST
COPY pyproject.toml uv.lock ./

# 🔥 Install uv
RUN pip install --no-cache-dir uv

# 🔥 Install dependencies from pyproject
RUN uv pip install --system .

# Copy rest of project
COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]