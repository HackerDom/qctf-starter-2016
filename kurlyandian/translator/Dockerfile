FROM golang:latest

COPY . /app

WORKDIR /app/translator
RUN go build

CMD [ "./translator" ]
