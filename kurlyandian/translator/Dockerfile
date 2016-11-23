FROM golang:latest

COPY . /app

WORKDIR /app
RUN go build

CMD [ "./app" ]

EXPOSE 8080
