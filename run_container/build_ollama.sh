#!/bin/bash
start_time=$(date +%s)
docker build . -f ./run_container/Dockerfile -t ollama_xyz 
end_time=$(date +%s)
echo "Walltime: $((end_time - start_time)) seconds"
