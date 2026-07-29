FROM python:3.12-slim
LABEL authors="david"

COPY comune ./comune
COPY clientdir ./clientdir
ADD run-client.sh .
#ADD clientdir/client.py .
CMD [ "/bin/bash" ,"./run-client.sh" ]