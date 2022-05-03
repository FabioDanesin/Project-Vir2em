FROM python:3.9-alpine 
#Distro alpine con python 3.9

ENV PYTHONDIRECTORY=/vir2em/python

RUN mkdir -p ${PYTHONDIRECTORY}
WORKDIR ${PYTHONDIRECTORY}
RUN pip3 install -Ur Requirements.txt

COPY .. .

EXPOSE 6000

RUN python3 MainPage.py
