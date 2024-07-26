#!/bin/sh

# load credentials from .env
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

SERVER="$USER@$IP"
DEPLOY_PATH="/data/proj/"

# Sync file with production server
sshpass -p "$SSH_PASSWORD" rsync -e 'ssh -p $PORT' -avz --delete --exclude '.git*' . $SERVER:$DEPLOY_PATH

# Post-deployment commands
sshpass -p "$SSH_PASSWORD" ssh -p $PORT -tt $SERVER << 'ENDSSH'
cd /data/proj/
docker-compose up --build -d
ENDSSH
