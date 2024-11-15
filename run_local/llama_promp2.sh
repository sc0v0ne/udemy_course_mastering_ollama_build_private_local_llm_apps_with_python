#!/bin/bash
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "tell me  fun fact about Mozambiq"}], "stream": false}'