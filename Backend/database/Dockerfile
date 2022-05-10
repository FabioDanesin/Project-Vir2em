FROM postgres:latest

# TODO: postgres non accetta connessioni
ENV DATA=/var/lib/postgresql/
ENV DUMPFILE=alldump.sql
RUN mkdir -p ${DATA}
WORKDIR ${DATA}
COPY alldump.sql .
