#   ./django/Dockerfile
FROM python:3.14.6-bookworm
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements_dev.txt .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements_dev.txt
COPY . .
RUN adduser --disabled-password --gecos '' investimento
RUN chown -R investimento:investimento /app
USER investimento