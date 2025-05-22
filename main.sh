#!/bin/bash

# Exit the script immediately on error
set -e

# Run the generator (waits to finish)
python3 src/main.py

# Only if that succeeded, serve the site
cd public
python3 -m http.server 8888
