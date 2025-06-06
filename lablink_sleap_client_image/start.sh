#!/bin/bash

echo "Starting the lablink sleap client container..."

echo "ALLOCATOR_HOST: $ALLOCATOR_HOST"
echo "TUTORIAL_REPO_TO_CLONE: $TUTORIAL_REPO_TO_CLONE"

if [ -n "$TUTORIAL_REPO_TO_CLONE" ]; then
  cd /home/client/Desktop
  echo "Cloning repository $TUTORIAL_REPO_TO_CLONE..."
  sudo -u client git clone "$TUTORIAL_REPO_TO_CLONE"
else
  echo "TUTORIAL_REPO_TO_CLONE not set. Skipping clone step."
fi

echo "Running subscribe script..."

# Activate the conda environment and run the subscribe script
/home/client/miniforge3/bin/conda run -n base subscribe allocator.host=$ALLOCATOR_HOST

# Keep the container alive
tail -f /dev/null