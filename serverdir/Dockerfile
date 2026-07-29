FROM python:3.15.0b4-alpine3.24
LABEL authors="david"
#SHELL ["bash", "-c"]
COPY comune ./comune
ADD serverdir/server.py .
RUN apk update && apk add make gcc g++

CMD ["python3", "-m" , "server"]