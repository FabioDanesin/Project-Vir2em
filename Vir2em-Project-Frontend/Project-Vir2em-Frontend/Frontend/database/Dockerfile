FROM postgres:latest

ENV DUMP=alldump.sql
ENV DUMPDIR=/etc/var/dump

RUN mkdir -p /${DUMPDIR}
WORKDIR ${DUMPDIR}

COPY ${DUMP} .

RUN psql -U postgres -f ${DUMP}
