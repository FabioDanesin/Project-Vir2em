Per installare tutte le librerie insieme usate nel progetto tramite pip3:
pip3 install -Ur requirements.txt 

PER L'ERRORE DI PSYCOPG2: 
Linux: 
  scrivere sul terminal :
  sudo apt-get install libpq-dev
  pip install psycopg2
  
  se l'ultimo comando non dovesse comunque funzionare, scaricare il file .tar di psycopg2 manualmente e riprovare
  
 Windows: 
  trovare il path a cui psycopg2 dovrebbe essere installato(sapete di essere nella cartella corretta quando nei file di sqlalchemy trovate "import psycopg2" scritto negli import e inserire il file li. 

PEM PASSPHRASE: 
  plc20212022