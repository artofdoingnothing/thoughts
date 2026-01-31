FROM python:3.11-slim

WORKDIR /app

COPY workers/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# We need the backend module for the shared database models
# In a real monorepo, we might use a shared library
# For now, we'll assume the entire monorepo root is context or handle with compose
ENV PYTHONPATH=/app

CMD ["python", "-m", "workers.worker"]
