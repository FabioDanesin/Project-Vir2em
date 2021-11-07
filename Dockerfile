
#Immagine di base
FROM httpd:latest
RUN pip install --upgrade pip

#Copia e installa requirements
COPY ./requirements.txt /var/www/apache-flask-server/requirements.txt
RUN pip install -r /var/www/apache-flask-server/requirements.txt

#ROOT=/var/www/apache-flask-server/
#Copia configurazione apache
COPY Frontend/Docker/apache-flask-server.conf /var/www/apache-flask-server/apache-flask-config.conf
RUN a2ensite apache-flask-server
RUN a2enmod headers

#Copia file wsgi
COPY Frontend/Docker/apache-flask-server.wsgi /var/www/apache-flask-server/apache-flask-server.wsgi

COPY Frontend/MainPage.py /var/www/apache-flask-server/MainPage.py
COPY  Frontend/Templates /var/www/apache-flask-server/Templates

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80

WORKDIR /var/www/apache-flask-server

CMD /usr/sbin/apache2ctl -D FOREGROUND