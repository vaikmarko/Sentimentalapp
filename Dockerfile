FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Laadi alla NLTK andmed buildi käigus
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

COPY . .

ENV PORT=8080

CMD ["python", "startup.py"] 