#!/bin/bash

if [[ $1 == dev ]]; then
    docker-compose -f docker-compose.yaml up
elif [[ $1 == dev-rebuild ]]; then
    docker-compose -f docker-compose.yaml up --build app
elif [[ $1 == clear ]]; then
    docker-compose -f docker-compose.yaml down -v
elif [[ $1 == migrate ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic revision --autogenerate -m "$2"
elif [[ $1 == upgrade ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic -x data=true upgrade  $2
elif [[ $1 == downgrade ]]; then
    docker-compose -f docker-compose.yaml run --rm app alembic -x data=true downgrade $2
elif [[ $1 == test ]]; then
    docker-compose -f docker-compose.test.yaml down -v
    docker-compose -f docker-compose.test.yaml up --exit-code-from app-test
elif [[ $1 == test-rebuild ]]; then
    docker-compose -f docker-compose.test.yaml down -v
    docker-compose -f docker-compose.test.yaml up --exit-code-from app-test --build app-test
fi
