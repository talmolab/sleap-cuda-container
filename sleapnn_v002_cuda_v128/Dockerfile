# Base image with GPU support
FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04

# Set working directory
WORKDIR /app

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Set user
ENV USER=root

# Set NVIDIA driver capabilities
ENV NVIDIA_DRIVER_CAPABILITIES=all

# Set QT debug environment variable to help debug issues with Qt plugins
ENV QT_DEBUG_PLUGINS=1

# Set virtual environment
ENV VIRTUAL_ENV=/app/.venv

# Install uv + dependencies
# opencv requires opengl https://github.com/conda-forge/opencv-feedstock/issues/401
# Default python3 is 3.8 in ubuntu 20.04 https://wiki.ubuntu.com/FocalFossa/ReleaseNotes#Python3_by_default
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    # libgl1-mesa-glx \
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
    python3 \
    python3-venv \
    python3-pip \
    git \
    curl && \
    # python3-pip && \
    # python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Initialize uv project
RUN uv init --no-readme

# Create virtual env w/ Python 3.13
RUN uv venv --python 3.13

# Set virtual environment path
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# # Add MarkupSafe from git
RUN uv add git+https://github.com/pallets/markupsafe@3.0.2

# Install sleap-nn w/ CUDA 12.8 support
RUN uv add "sleap-nn[torch-cuda128]" --index https://download.pytorch.org/whl/cu128 --index https://pypi.org/simple