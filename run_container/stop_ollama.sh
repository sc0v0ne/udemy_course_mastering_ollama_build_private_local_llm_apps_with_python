#!/bin/bash
start_time=$(date +%s)
docker stop container-mario
end_time=$(date +%s)
echo "Walltime: $((end_time - start_time)) seconds"
