FROM python:3

COPY public.pem /app/public.pem
COPY server.py /app/server.py

RUN pip install rsa
WORKDIR /app
CMD [ "python", "./server.py", "-p", "9081" ]

EXPOSE 9081
