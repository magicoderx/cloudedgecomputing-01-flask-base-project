#!/bin/sh

# load credentials from .env
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

SERVER="root@3.74.7.83"
DEPLOY_PATH="/data/proj/"

# Sync file with production server
sshpass -p "$SSH_PASSWORD" rsync -e 'ssh -p 3224' -avz --delete --exclude '.git*' . $SERVER:$DEPLOY_PATH

# Post-deployment commands
sshpass -p "$SSH_PASSWORD" ssh -p 3224 -tt $SERVER << 'ENDSSH'
cd /data/proj/
docker-compose down
docker-compose up --build -d
ENDSSH
