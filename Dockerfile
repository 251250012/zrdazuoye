FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data

EXPOSE 8080

ENV SECRET_KEY=change-this-in-production

CMD ["python", "app.py"]