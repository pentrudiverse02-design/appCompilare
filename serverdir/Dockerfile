FROM python:3.15.0b4-alpine3.24
LABEL authors="david"

COPY comune ./comune
ADD server.py .
install gcc
CMD ["python3", "-m" , "server"]