#!/bin/sh

# load credentials from .env
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

SERVER="root@3.74.7.83"
DEPLOY_PATH="/data/proj/"

# Sync file with production server
sshpass -p "$SSH_PSWD" rsync -e 'ssh -o StrictHostKeyChecking=no -p 3224' -avz --delete --exclude '.git*' . $SERVER:$DEPLOY_PATH

# Post-deployment commands
sshpass -p "$SSH_PSWD" ssh -o StrictHostKeyChecking=no -p 3224 -tt $SERVER << 'ENDSSH'
cd /data/proj/
docker-compose down
docker-compose up --build -d
exit
ENDSSH
