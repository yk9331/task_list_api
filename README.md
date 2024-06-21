# Task List API

[![Test](https://github.com/yk9331/task_list_api/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/yk9331/task_list_api/actions/workflows/test.yml)
[![Lint](https://github.com/yk9331/task_list_api/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/yk9331/task_list_api/actions/workflows/lint.yml)


A task list api project with FastAPI and MySQL

## Technologies
RESTful API
- Language: **Python 3.10**
- Framework: **FastAPI 0.111**

Database
- MySQL
- ORM : SQLAlchemy 2.0
- Migration : Alembic

Others
- Dependency Management: Poetry
- Test Framework: pytest
- Linter: pre-commit
- Container: Docker, Docker-Compose
- Documents: Open API spec (Swagger/Redoc)
- CI: Github Action

## Run locally

1. Devlopment - start server with docker-compose (server will reload when code changed)

    - Run `sh docker.sh dev`
    - Run `sh docker.sh dev-rebuild` if package updated

2. Test - run test with docker-compose

    - Run  `sh docker.sh test`
    - Run  `sh docker.sh test-rebuild` if package updated

## Project Structure
```
├── .github
│   └── workflows         // github action scripts
├── alembic               // db migration scripts
├── src
│   ├── controllers       // db crud controller
│   ├── core              // general resource(config, auth, exceptions...)
│   │   └── db            // db orm setting
│   ├── models            // db schema
│   ├── routers           // api router definition
│   │   └── endpoints     // endpoint definitaion
│   ├── schemas           // request/response schema
│   └── main.py           // app entry point
└── tests                 // api intergration test, unit test
    ├── test_api          // api intergration test
    └── utils             // test utility
        └── dummy_data    // test dummy data
```

## API Endpoints
Full Document:
- Swagger: [API_HOST]/docs
- Redoc: [API_HOST]/redoc

Public Endpoints:
```
POST    /v1/user/login  get access token with name
```

Private Endpoints (with Bearer Authentication):
```
GET     /v1/tasks       get task list
POST    /v1/task        create task
PUT     /v1/task/{id}   update task
DELETE  /v1/task/{id}   delete task
```

## Dockerfile Best Practice
Use slim image and multi-stage build to reduce final image size from 1.23GB to 206 MB
