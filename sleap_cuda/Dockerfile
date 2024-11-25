# Base image with GPU support
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Set user
ENV USER=root

# Set NVIDIA driver capabilities
ENV NVIDIA_DRIVER_CAPABILITIES=all

# Set QT debug environment variable to help debug issues with Qt plugins
ENV QT_DEBUG_PLUGINS=1

# Install dependencies
# opencv requires opengl https://github.com/conda-forge/opencv-feedstock/issues/401
# Default python3 is 3.8 in ubuntu 20.04 https://wiki.ubuntu.com/FocalFossa/ReleaseNotes#Python3_by_default
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglapi-mesa \
    libegl-mesa0 \
    libegl1 \
    libopengl0 \
    libglib2.0-0 \
    libfontconfig1 \
    libgssapi-krb5-2 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxkbcommon-x11-0 \
    python3-pip && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install SLEAP
RUN pip install --no-cache-dir sleap[pypi]==1.3.4