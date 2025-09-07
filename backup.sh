#!/bin/bash
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR
docker-compose exec -T db pg_dump -U interview_user interview_app > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql
