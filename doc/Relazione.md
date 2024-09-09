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
in modo da avere a disposizione le librerie utili al corretto funzionamento dell'applicazione.

## Funzionamento applicazione
### Installazione e configurazione del database
Per interagire con il database postgres (per il conteggio delle visualizzazioni del blog) bisogna installare postgres sul proprio dispositivo e creare un database iniziale.

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
[![CI Pipeline](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/actions/workflows/ci.yml/badge.svg)](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/actions/workflows/ci.yml)
### Test
Sono stati creati due test principali per ottenere informazioni sul corretto funzionamento dell'applicazione: test per le risposte http e test per la validazione della conformità dei markdown presenti in [posts/en/](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/tree/main/posts/en).

#### HTTP Test
Il test delle richieste HTTP utilizza python unittest per verificare sostanzialmente le risposte in 3 casi:
- Home Page: In questo caso si verifica che facendo una richiesta GET a '/' si ottenga il codice 200 OK. Inoltre si verifica che nella risposta sia presente la stringa 'Things I Can Do', che sappiamo essere presente nella landing page
- Post Page: Qui si verifica che accedendo a '/blog/my-first-freelance-exp' si ottenga un 200 OK, quindi che la pagina sia effettivamente visibile, e che nella response sia presente la stringa 'My first try at freelancing' che sappiamo esistere in questo specifico blog
- Pagina inesistente: Infine si fa un test tramite una GET verso una pagina inesistente e si verifica che questo restituisca un 404 Not Found

#### Test conformità markdown
Nel progetto esiste un [template](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/posts/template.md.tmpl) che rappresenta lo scheletro di un markdown scritto correttamente. Il template è molto semplice e vuole che le prime 9 righe abbiano dei campi ben specifici e alcuni richiedono un pattern del valore anch'esso specifico. Il test prende il contenuto dei file markdown presenti in 'posts/en/' e per ognuno si prendono le prime 9 righe e si verifica che queste righe contengano tutti i campi specificati nel template. Inoltre si verifica anche per alcuni campi come:  *author_image*, *date* e *image* che il pattern del valore matchi con quello specificato nel template (ad esempio i file delle immagini devono avere le opportune estensioni). Un'altra verifica che viene eseguita è la presenza della stringa '---' dopo questi campi.
###
Se TUTTI questi test passano con successo, allora il deploy può avvenire senza problemi.

### Docker
Per questo progetto si è pensato di utilizzare un container Docker per far girare l'applicazione in modo tale da avere un ambiente isolato per ragioni di sicurezza e di semplicità di sviluppo. Per Avviare il container è stato creato un [Dockerfile](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/Dockerfile) che utilizza la versione 3.9 slim di Python per avere un'immagine di dimensione ridotta contenente solo le librerie e i file essenziali per eseguire Python. Vengono successivamente installati tramite `pip install` delle dipendenze specificate nel file *requirements.txt*. Dopodiché si copiano tutti i flie e in particolare il kickstart viene spostato nella working directory.

#### Kickstart.sh
Il [kickstart](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/kickstart.sh) è uno script bash impostato come entrypoint del Dockerfile che esegue i comandi di avvio dell'applicazione, in particolare verifica se il parametro *RUN_TESTS* è vero: in questo caso esegue il test dell'HTTP (questo viene richiamato ovviamente in fase di testing e non di deploy), altrimenti esegue *gunicorn* per avviare l'applicazione.

### Docker compose
Dato che l'applicazione si basa su un database per salavre le informazioni riguardanti le visualizzazioni sui blog, l'idea è quella di creare un'altra immagine docker contenente un database postgres. Per fare in modo che i due container comunichino tra loro è stato scelto di implementare un [docker compose](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/docker-compose.yml) per orchestrare questi container. Il docker compose crea innanzitutto un'immagine "my-flask-app" che viene costruita dal Dockerfile e mappa la porta 80 (esterna) alla porta 8080 (dell'applicazione). È stato scelto di utilizzare la porta 80 esterna per creare una connessione standard (anche se obsoleta) in http. Questo container avrà come dipendenza il database che viene creato inizialmente impostando una variabile d'ambiente per postgresql. Il database sarà quindi costruito con un'immagine di postgres 13 impostando le credenziali di accesso e mappando la porta 5432 dall'esterno per una eventuale gestione. È stato scelto di creare una directory per la persistenza dei dati quando il compose viene eliminato e ricreato (come vedremo in fase di deploy).

Infine viene definito il test che crea un'immagine, appunto di test, costruita come se fosse un'app in produzione.

### Deploy
La fase finale del CI/CD è proprio il deploy dell'applicazione su un'istanza EC2 di AWS. Il deploy viene eseguito tramite un banale [script](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/deploy.sh) che controlla se ci sono o meno delle variabili nel file *.env* locale, ed esegue un rsync sulla macchina remota, copiando al suo interno tutti i file (tranne quelli di github in quanto non necessari). Dopodiché viene fatta una connessione ssh in cui viene spento il docker compose se attivo, per poi costruire quello aggiornato e far partire l'applicazione nel server remoto.

Per accedere al server remoto viene utilizzata una password che può trovarsi in locale allo sviluppatore in un file *.env* oppure, come in questo caso, all'interno dell'ambiente di github: più precisamente nella sezione *Secrets and variables*->*Actions*->*Repository secrets*, Per il deploy da github è stato scelto di utilizzare questo metodo grazie alla sicurezza fornita da GitHub stesso.

#### VM AWS
La Virtual Machine di AWS è ospitata su un server nella regione di Francoforte ed è un'istanza di tipo T2.small e a cui è attaccato un disco EBS in gp3 su cui è installato il sistema operativo CentOS Stream 9. È stata scelta una VM general purpose in quanto non richiede prestazioni particolari e specifiche. Per accedere a questa macchina in SSH si può accedere tramite una porta (non standard) sia con utente/password che tramite una chiave privata, e le porte dall'esterno sono gestite da un apposito Security Group a livello di istanza.

### CI/CD
Per gestire questo workflow è stato creato un file [ci](https://github.com/magicoderx/cloudedgecomputing-01-flask-base-project/blob/main/.github/workflows/ci.yml). Il flusso parte quando viene fatto un push al branch principale o quando fiene fatta una pull request sempre verso il branch main. Il primo job che viene eseguito è il test in cui, dopo aver ottenuto il codice dal repository, si configura un ambiente Python in cui vengono installate le dipendenze necessarie che si trovano nel file *requirements.txt*. Da qui parte il primo script Python per eseguire la validazione del markdown e il test per le risposte HTTP che crea un ambiente di testing con tanto di network in cui inserire il db e l'applicazione in modo che possano comunicare tra loro. Viene pulito poi tutto una volta terminato il test

Se il test va a buon fine si passa alla fase di deploy che sostanzialmente non fa altro che eseguire lo script del deploy su AWS. Qui viene impostata la variabile d'ambiente creata nei secrets del repository (la password che utilizzerà lo script per collegarsi in ssh)

Se anche il deploy va a buon fine si può ritenere completata con successo la pipeline CI/CD

## Sviluppi futuri
Attualmente il progetto tratta soltanto un'applicazione flask containerizzata, sarebbe interessante create un'automazione del monitoraggio, implementando degli strumenti per il monitoraggio continuo della performance e della sicurezza. Un'idea potrebbe essere quella di utilizzare una combinazione di Prometheus e Grafana per avere grafici su tutto ciò che può essere interessante monitorare. Questa soluzione potrebbe essere orchestrata da un orchestratore come Kubernetes per fornire eventuale scalabilità automatica e bilanciamento del carico per ridurre al minimo il tempo delle risposte (ed evitare un sovraccarico).

Utilizzando Kubernetes e/o un Docker compose con più container si potrebbe optare per utilizzare un servizio come [Portainer](https://www.portainer.io/) per avere una UI che permette allo sviluppatore di gestire in maniera semplice e rapida i vari container.

Infine, un'altro potenziale sviluppo futuro è l'implementazione di strategie di failover e disaster recovery per garantire alta disponibilità e l'alta affidabilità del sistema.
