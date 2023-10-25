FROM python:3-slim-buster  AS builder
ENV TZ="Asia/Shanghai"
#ENV PYTHONPATH=/app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt  --no-cache-dir

#RUN <<EOF
#apt-get update
#apt-get install -y --no-install-recommends git
#EOF



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
