# Schedule

The application based on pure [Python](https://www.python.org) and [Angular](https://angular.io) (the Google's JavaScript framework). With Schedule everyone can define, get, update and remove personal tasks.

## Installation and Configuration

Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/) to run the project through Docker. But it is not necessary, should to understand the logic: the `./server` directory refers to Python, the `./client` directory refers to Angular.

Before running, need to configure some environment variables.

### Server Side

Edit the `./server/src/env.py` file.

**Databases**

- `production_database_uri` - the URI of the production database
- `development_database_uri` - the URI of the development database

**CORS**

- `client_endpoint` - the URI of the client side

**JWT**

- `jwt_expiration_time` - the time in seconds then the JWT will expire

### Client Side

Edit the `./client/src/environment/environment.prod.ts` and `./client/src/environment/environment.ts` files.

**CORS**

- `serverEndpoint` - the URI of the client side

**Local Configuration**

- `beginningDate` - the date from which should to begin the task list creation

## Launching

Execute the `docker compose up` command from the `./docker` directory and then create the development database with the `docker compose exec -w /home/schedule/server/src python python -m init create development` command. Check your browser page, the request to `http://0.0.0.0:3000` should be successful.

Tests must be run using the `docker compose exec -w /home/schedule/server/src python python -m init test` and `docker compose exec -w /home/schedule/client node npm run test` commands for server and client sides respectively.

## Commands

In addition to standard [the Docker commands](https://docs.docker.com/engine/reference/run/), the Python part have the `init` module.

**Server Side**

- `docker compose exec -w /home/schedule/server/src python python -m init production create` - create production database
- `docker compose exec -w /home/schedule/server/src python python -m init production delete` - drop production database
- `docker compose exec -w /home/schedule/server/src python python -m init development create` - create development database
- `docker compose exec -w /home/schedule/server/src python python -m init development delete` - drop development database
- `docker compose exec -w /home/schedule/server/src python python -m init test` - run tests

**Client Side**

- `docker compose exec -w /home/schedule/client node npm run start` - launch the application
- `docker compose exec -w /home/schedule/client node npm run build` - build the application
- `docker compose exec -w /home/schedule/client node npm run test` - run unit tests
