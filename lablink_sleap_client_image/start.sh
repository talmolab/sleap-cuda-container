#!/bin/bash

echo "Running subscribe script..."

# Activate the conda environment and run the subscribe script
/home/client/miniforge3/bin/conda run -n base subscribe allocator.host=$ALLOCATOR_HOST

# Keep the container alive
tail -f /dev/null