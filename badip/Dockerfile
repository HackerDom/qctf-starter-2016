FROM python:3

COPY public.pem /
COPY server.py /

RUN pip install rsa
CMD [ "python", "./server.py", "-p", "9081" ]

EXPOSE 9081
