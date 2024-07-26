# Relazione Progetto Cloud and Edge Computing
## Introduzione
Il presente progetto è un fork di un branch del progetto presente nel GitLAB del professor Francesco Faenza (https://gitlab.com/frfaenza/cloudedgecomputing/-/tree/01-flask-base-project). Lo scopo del progetto è quello di creare una pagina web che funge da blog/Curriculum Vitae online. Aprendo la pagina web si arriva in una landing page in cui appare l'About Me e competenze del professore. Scorrendo in basso troviamo una sezione (blog) contenente una sua esperienza da freelancer; cliccando su "Continue Reading" si viene reindirizzati alla sezione blog in cui viene spiegata in dettaglio la sua esperienza. Gli accessi a questo blog vengono poi memorizzati in un database per avere uno storico di informazioni riguardo le visualizzazioni.

## Idea
Essendo un progetto già funzionante, con il presente progetto ci si concentra sulla parte di DevOps e della creazione di una Pipeline CI/CD per automatizzare il processo di test e di deploy. L'idea generale è quella di implementare degli Unit Tests sulle richieste HTTP e sulla correttezza del markdown in fase di deploy. Dopodiché verrebbe effettuato il deploy dell'applicazione su una VM (EC2) in AWS che renderà disponibile l'applicazione tramite un'immagine docker.

Dunque e implementazioni dovrebbero implementare:
- Un *Dockerfile* che contiene l'esecuzione della parte web Flask
- Un *docker-compose.yml* per orchestrare l'app Flask e il database che utilizza
- Un *.github-ci.yml* per testare, e fare deploy del progetto