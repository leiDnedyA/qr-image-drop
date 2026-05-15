FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    UPLOAD_FOLDER=/app/static/images \
    COUNTER_FILE=/app/data/counter.txt

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libde265-0 libglib2.0-0 libheif1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static/images /app/data \
    && chown -R 10001:10001 /app/static/images /app/data

USER 10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f\"http://127.0.0.1:{os.environ.get('PORT', '8080')}/vet\", timeout=3).read()" || exit 1

CMD ["sh", "-c", "gunicorn --workers ${WEB_CONCURRENCY:-1} --threads ${WEB_THREADS:-8} --bind 0.0.0.0:${PORT:-8080} app:app"]
