#!/bin/bash

python3 -c server.py 

echo "Server started"

# wait for the server to send msg to worker to start
docker run --rm -t -p 8080:8080 

# start client
python -c client.py