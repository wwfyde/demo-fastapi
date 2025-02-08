FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

ENV TZ="Asia/Shanghai"
#ENV PYTHONPATH=/app

WORKDIR /app

COPY . .

RUN uv sync

#RUN <<EOF
#apt-get update
#apt-get install -y --no-install-recommends git
#EOF



CMD ["uv","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
