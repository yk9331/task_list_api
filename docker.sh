#!/bin/bash

if [[ $1 == dev ]]; then
    docker-compose -f docker-compose.yaml up
elif [[ $1 == rebuild ]]; then 
    docker-compose -f docker-compose.yaml up --build app
elif [[ $1 == clear ]]; then
    docker-compose -f docker-compose.yaml down -v
elif [[ $1 == migrate ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic revision --autogenerate -m "$2"
elif [[ $1 == upgrade ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic -x data=true upgrade  $2
elif [[ $1 == downgrade ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic -x data=true downgrade $2
fi