FROM python:3.5

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 80
