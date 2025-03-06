FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python init_db.py

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]