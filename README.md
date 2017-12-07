# AltiSolve

The repo is a production ready app, that uses `nginx` to serve static files (the client app and static files from the server), and `gunicorn` for the server (python) stuff. All the parts are in a separate [Docker](https://www.docker.com/) containers and we use [kubernetes](https://kubernetes.io/) to manage them.

## Pre Requirements

1. install [docker](https://www.docker.com/).

## Installation

Automatic installation of the project with docker, for development.

1. In `client` directory run `docker build -t client .` to build the Docker image.
2. Run ```docker run -dit -v `pwd`:/usr/src -p 4200:4200 --name=client-con client``` to run a container from that image.
3. Open the browser at [http://localhost:4200](http://localhost:4200) to see your Angular (client) app.
4. In `server` directory run `docker build -t server .` to build the Docker image.
5. Run ```docker run -dit -v `pwd`:/usr/src -p 8000:8000 --name=server-con server``` to run a container from that image.
6. Open the browser at [http://localhost:8000](http://localhost:8000) to see your Django (server) app.

If you want to install the project manually, go to the `/client` or `/server` directories and read the `README` file.

## Our Stack

* [Angular](https://angular.io/)
* [Django](https://www.djangoproject.com/)
* [PostgreSQL](http://www.postgresql.org/)
* [Docker](https://www.docker.com/)

**Tools we use**

  * [Angular Material](https://material.angular.io/)
  * [ngrx](https://github.com/ngrx)
  * [Django REST framework](http://www.django-rest-framework.org/)
  * [kubernetes](https://kubernetes.io/)

## Contribute

Altimetrik