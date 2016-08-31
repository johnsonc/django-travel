#!/bin/bash

function build {
        echo  "Building image.."
        docker build -t travel-django-app django-app
}

function start {
        echo "Starting container..."
        # Start travel microservice in Docker with 8000 port
        docker run -p 8000:8000 -it --rm --name travel-django travel-django-app
}

function startdaemon {
        echo "Starting container..."
        # Start travel microservice in Docker with 8000 port
        docker run -p 8000:8000 -d --name travel-django travel-django-app
}

case "$1" in
   start)
      start
   ;;
   start-daemon)
      startdaemon
   ;;
   build)
      build
   ;;
   *)
      echo "Usage: $0 start|start-daemon|build"
esac