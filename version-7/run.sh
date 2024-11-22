#!/bin/bash

python3 client.py
gnome-terminal --tab -- bash -c "python3 server.py; exec bash"
