#!/bin/bash

CONTAINER=$(docker ps | grep 'rrey/reminder_api'|awk '{print $1}')
[ -n "$CONTAINER" ] && echo "Container already running" && exit 0

docker pull rrey/reminder_api
[ $? -ne 0 ] && exit 1

docker run -it --rm -p 8000:8000 -d rrey/reminder_api
exit $?
