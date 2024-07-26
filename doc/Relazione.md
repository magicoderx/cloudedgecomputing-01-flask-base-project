# Relazione Progetto Cloud and Edge Computing
## Introduzione
Il presente progetto è un fork di un branch del progetto presente nel GitLAB del professor Francesco Faenza (https://gitlab.com/frfaenza/cloudedgecomputing/-/tree/01-flask-base-project). Lo scopo del progetto è quello di creare una pagina web che funge da blog/Curriculum Vitae online. Aprendo la pagina web si arriva in una landing page in cui appare l'About Me e competenze del professore. Scorrendo in basso troviamo una sezione (blog) contenente una sua esperienza da freelancer; cliccando su "Continue Reading" si viene reindirizzati alla sezione blog in cui viene spiegata in dettaglio la sua esperienza. Gli accessi a questo blog vengono poi memorizzati in un database per avere uno storico di informazioni riguardo le visualizzazioni.

## Idea
Essendo un progetto già funzionante, con il presente progetto ci si concentra sulla parte di DevOps e della creazione di una Pipeline CI/CD per automatizzare il processo di test e di deploy. L'idea generale è quella di implementare degli Unit Tests sulle richieste HTTP e sulla correttezza del markdown in fase di deploy. Dopodiché verrebbe effettuato il deploy dell'applicazione su una VM (EC2) in AWS che renderà disponibile l'applicazione tramite un'immagine docker.

Dunque le implementazioni dovrebbero comprendere:
- Un *Dockerfile* che contiene l'esecuzione della parte web Flask
- Un *docker-compose.yml* per orchestrare l'app Flask e il database che utilizza
- Degli script Python in *unittest* o *pytest*  
- Un *.github-ci.yml* per testare, e fare deploy del progetto 

## Preparazione
Per utilizzare questa applicazione è necessario avere python installato all'interno del proprio PC. Dopodiché si installano le dipendenze presenti in [requirements.txt](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/requirements.txt) tramite il comando
```
pip install -r requirements.txt
```
in modo da avere a disposizione le librerie utili al corretto funzionamento dell'applicazione

## Funzionamento applicazione
### Installazione e configurazione del database
Per interagire con il database postgres (per il conteggio delle visualizzazioni del blog) bisogna installare postgres sul proprio dispositivo e creare un database iniziale

In alternativa si può lanciare un database dockerizzato tramite il seguente comando (ovviamente bisogna avere docker installato sul sistema)
```shell
docker run --rm --name flask-db-test -e POSTGRES_PASSWORD=passwordhere -e POSTGRES_USER=flask -e POSTGRES_DB=blog postgres
```

### Avvio applicazione
Per avviare l'applicazione basta eseguire i seguenti comandi da linea di comando
```shell
export FLASK_APP=app.py
flask db init
flask db migrate
flask db upgrade
gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
```

## Sviluppo del progetto di DevOps
### Test
Sono stati creati due test principali per ottenere informazioni sul corretto funzionamento dell'applicazione: test per le risposte http e test per la validazione della conformità dei markdown presenti in [posts/en/](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/tree/main/posts/en)

#### HTTP Test
Il test delle richieste HTTP utilizza python unittest per verificare sostanzialmente le risposte in 3 casi:
- Home Page: In questo caso si verifica che facendo una richiesta GET a '/' si ottenga il codice 200 OK. Inoltre si verifica anche che nella riasposta sia presente la stringa 'Things I Can Do', che sappiamo essere presente nella landing page
- Post Page: Qui si verifica che accedendo a '/blog/my-first-freelance-exp' si ottenga un 200 OK, quindi che la pagina sia effettivamente visibile, e che nella response sia presente la stringa 'My first try at freelancing' che sappiamo esistere in questo specifico blog
- Pagina inesistente: Infine si fa un test tramite una GET verso una pagina inesistente e si verifica che questo restituisca un 404 Not Found

#### Test conformità markdown
Nel progetto esiste un [template](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/posts/template.md.tmpl) che rappresenta lo scheletro di un markdown scritto correttamente. Il template è molto semplice e vuole che le prime 9 righe abbiano dei campi ben specifici e alcuni richiedono un pattern del valore anch'esso specifico. Il test prende il contenuto dei file markdown presenti in 'posts/en/' e per ognuno si prendono le prime 9 righe e si verifica che queste righe contengano tutti i campi specificati nel template. Inoltre si verifica anche per alcuni campi come:  *author_image*, *date* e *image* che il pattern del valore matchi con quello specificato nel template (ad esempio i file delle immagini devono avere le opportune estensioni). Un'altra verifica che viene eseguita è la presenza della stringa '---' dopo questi campi
###
Se TUTTI questi test passano con successo, allora il deploy può avvenire senza problemi

### Docker