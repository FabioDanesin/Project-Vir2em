FROM postgres:latest


ENV DATA=/var/lib/postgres
WORKDIR ${DATA}
COPY ${DATA} .

### VECCHIO
#ENV DUMP=alldump.sql
#ENV DUMPDIR=/etc/var/dump
#
#RUN mkdir -p /${DUMPDIR}
#WORKDIR ${DUMPDIR}
#
#COPY ${DUMP} .
#
#RUN psql -U postgres -f ${DUMP}
