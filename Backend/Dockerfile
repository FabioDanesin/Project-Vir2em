FROM ubuntu:latest
# Distro alpine con python 3.9

ENV PYTHONDIRECTORY=/vir2em/python
# Il flag -p crea anche il path del parent se non esiste
RUN mkdir -p ${PYTHONDIRECTORY}

# Cambio directory nel container e copio l'intero progetto
WORKDIR ${PYTHONDIRECTORY}
COPY . .

# Aggiorno la lista dei pacchetti
RUN apt-get update

# Pip e l'interprete di python
RUN apt-get install -y python3 python3-pip

# Installo il resto dei pacchetti
RUN pip3 install -Ur Requirements.txt

# Lancio l'app
ENTRYPOINT [ "python3" , "MainPage.py"]