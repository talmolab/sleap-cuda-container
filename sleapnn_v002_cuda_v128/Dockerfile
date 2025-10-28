# # Base image with GPU support
# FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

# # Set working directory
# WORKDIR /app

# # Set non-interactive mode
# ENV DEBIAN_FRONTEND=noninteractive

# # Set user
# ENV USER=root

# # Set NVIDIA driver capabilities
# ENV NVIDIA_DRIVER_CAPABILITIES=all

# # Set QT debug environment variable to help debug issues with Qt plugins
# ENV QT_DEBUG_PLUGINS=1

# # Set virtual environment
# ENV VIRTUAL_ENV=/app/.venv

# # Install uv + dependencies
# # opencv requires opengl https://github.com/conda-forge/opencv-feedstock/issues/401
# # Default python3 is 3.8 in ubuntu 20.04 https://wiki.ubuntu.com/FocalFossa/ReleaseNotes#Python3_by_default
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     libgl1 \
#     libglx0 \
#     libglapi-mesa \
#     libegl-mesa0 \
#     libegl1 \
#     libopengl0 \
#     libglib2.0-0 \
#     libfontconfig1 \
#     libgssapi-krb5-2 \
#     libdbus-1-3 \
#     libx11-xcb1 \
#     libxkbcommon-x11-0 \
#     python3 \
#     python3-venv \
#     python3-pip \
#     git \
#     curl && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# # Install uv
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
#     && ln -s /root/.local/bin/uv /usr/local/bin/uv

# # Initialize uv project
# RUN uv init --python 3.13 --no-readme

# # Create virtual env w/ Python 3.13
# RUN uv venv

# # Set virtual environment path
# ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PIP_NO_CACHE_DIR=1

# # Add MarkupSafe from git
# RUN uv add git+https://github.com/pallets/markupsafe@3.0.2

# # Clean up apt cache and unnecessary files to free space
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# # Install sleap-nn w/ CUDA 12.8 support
# RUN uv add sleap-nn[torch] --index https://download.pytorch.org/whl/cu128 --index https://pypi.org/simple --no-cache

# Base image with GPU support (runtime variant instead of devel)
FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

# Set working directory
WORKDIR /app

# Non-interactive APT
ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV VIRTUAL_ENV=/app/.venv

# Install required system packages (minimal)
# - keep build-essential if you need to compile any local extensions,
#   otherwise remove it to speed installs
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglx0 \
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
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install uv, init project, create venv, and install Python deps in one layer
# Need to pin markupsafe to 3.0.2 due to compatibility issues with later versions
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -s /root/.local/bin/uv /usr/local/bin/uv \
 && uv init --python 3.13 --no-readme \
 && uv venv \
 && export PATH="/app/.venv/bin:$PATH" \
 && uv add "markupsafe==3.0.2" \
 && uv add "sleap-nn[torch]" --index https://download.pytorch.org/whl/cu128 --index https://pypi.org/simple --no-cache

# Environment for virtualenv usage
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1