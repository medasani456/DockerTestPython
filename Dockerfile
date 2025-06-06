FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
