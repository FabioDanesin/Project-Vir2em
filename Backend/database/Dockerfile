FROM postgres:latest


ENV DATA=/var/lib/postgresql/
ENV DUMPFILE=alldump.sql
RUN mkdir -p ${DATA}
WORKDIR ${DATA}
COPY alldump.sql .
