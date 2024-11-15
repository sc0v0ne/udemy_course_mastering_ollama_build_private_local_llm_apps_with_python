#!/bin/bash
SECONDS=0
DOCKER_BUILDKIT=1 docker exec -it container-mario bash mario.sh

duration=$SECONDS
echo "$((duration / 60)) minutes"