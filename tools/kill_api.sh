#!/bin/bash

CONTAINER=$(docker ps | grep 'rrey/reminder_api'|awk '{print $1}')
[ -z "$CONTAINER" ] && exit 0

docker kill $CONTAINER
exit $?
