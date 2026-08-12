#!/bin/sh
#   ./django/entrypoint.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "${BLUE}========================================${NC}"
echo "${BLUE}   Iniciando aplicação Django${NC}"
echo "${BLUE}========================================${NC}"

echo "${YELLOW}→ Collectstatic${NC}"
python manage.py collectstatic --noinput

echo "${YELLOW}→ Makemigrations${NC}"
python manage.py makemigrations

echo "${YELLOW}→ Migrate${NC}"
python manage.py migrate

echo "${YELLOW}→ Criando administrador${NC}"
python manage.py create_admin

echo "${GREEN}✓ Inicialização concluída${NC}"

exec python manage.py runserver 0.0.0.0:8000
