#!/bin/sh

# Executa as migrações do banco 
poetry run alembic upgrade head

# inicia a aplicação
poetry run fastapi run fast_zero/app.py