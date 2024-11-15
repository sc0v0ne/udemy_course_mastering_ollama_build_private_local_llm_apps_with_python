#!/bin/bash
start_time=$(date +%s)
bash ./run_container/build_ollama.sh
DOCKER_BUILDKIT=1  docker run --rm -p 3636:3636 --name container-mario -d ollama_xyz:latest
end_time=$(date +%s)
echo "Walltime: $((end_time - start_time)) seconds"
