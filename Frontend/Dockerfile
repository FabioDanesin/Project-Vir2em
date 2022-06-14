FROM nginx:1.14.2

# Path da creare
ENV ROOT=/var/log/nginx/vir2em

# Path interno per file .log e .conf
ENV FILES=src/nginx

# Crea tutte le directory comprese nel path se non esistono già
RUN mkdir -p ${ROOT}

WORKDIR ${ROOT}

# Comandi in bash per la creazione degli error e access log corrispondenti.
RUN mkdir ./error ./access
RUN touch error/error.log access/access.log

# Copio i vari log e .conf
COPY ${FILES}/nginx.conf /etc/nginx/nginx.conf
COPY ${FILES}/access.log access/access.log
COPY ${FILES}/error.log  error/error.log

