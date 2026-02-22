FROM python:3.11-slim

WORKDIR /app

COPY workers/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip \
    && wget -qO /tmp/cornell_dataset.zip http://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip \
    && mkdir -p /dataset/cornell_dialogs \
    && unzip -q /tmp/cornell_dataset.zip -d /dataset/cornell_dialogs \
    && rm /tmp/cornell_dataset.zip \
    && apt-get remove -y wget unzip \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# We need the backend module for the shared database models
# In a real monorepo, we might use a shared library
# For now, we'll assume the entire monorepo root is context or handle with compose
ENV PYTHONPATH=/app

CMD ["python", "-m", "workers.worker"]
