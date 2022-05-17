FROM python:3.9-alpine 
#Distro alpine con python 3.9

ENV PYTHONDIRECTORY=/vir2em/python

RUN mkdir -p ${PYTHONDIRECTORY}
WORKDIR ${PYTHONDIRECTORY}
COPY . .

#No cache -> non mantiene una copia del package index
RUN apk add --no-cache build-base libffi-dev libpq-dev 
RUN pip3 install -Ur Requirements.txt

ENTRYPOINT [ "python3" , "MainPage.py"]