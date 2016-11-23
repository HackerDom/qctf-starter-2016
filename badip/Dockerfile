FROM python:3

COPY public.pem /app
COPY server.py /app

WORKDIR /app
RUN pip install rsa
CMD [ "python", "./server.py", "-p", "9081" ]

EXPOSE 9081
