#!/bin/bash
# Start Nginx in the background
nginx &

# Wait for Nginx to be ready (optional, but recommended)
# You can add a loop to check Nginx's status or wait for a specific port
sleep 5 # Adjust as needed

# Execute your Python script
python3 /python-docker/main.py

# Keep the container running by tailing Nginx logs or a dummy file
tail -f /var/log/nginx/access.log
