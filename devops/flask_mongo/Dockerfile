FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# SQLite file location. Mount a volume here (compose: named volume, ECS: EFS)
# or the data disappears with the container.
ENV DB_PATH=/data/app.db
RUN mkdir -p /data

EXPOSE 5000

CMD ["python", "app.py"]
