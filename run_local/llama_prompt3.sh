#!/bin/bash
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "prompt":"WHat color is the sky at different times of the day? Respond using JSON", "format": "json", "stream": false}'