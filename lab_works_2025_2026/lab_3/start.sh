#!/bin/bash
# Start the Python ML server in the background
python3 /app/async_server.py &

# Start the SSH daemon in the foreground to keep the container alive
/usr/sbin/sshd -D
