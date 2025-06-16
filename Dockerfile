FROM python:3.10-slim

# Install build tools required for some Python packages (e.g. Firestore) on slim image
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during build to avoid runtime SSL issues
RUN python - <<'PY'
import ssl, nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except AttributeError:
    pass
for pkg in ("punkt", "stopwords", "vader_lexicon"):
    nltk.download(pkg)
PY

COPY . .

ENV PORT=8080

CMD ["python", "startup.py"] 