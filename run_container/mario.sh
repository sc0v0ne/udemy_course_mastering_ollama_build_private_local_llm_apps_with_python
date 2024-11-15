#!/bin/bash
SECONDS=0
ollama create mario -f Modelfile
ollama run mario
duration=$SECONDS
echo "$((duration / 60)) minutes"