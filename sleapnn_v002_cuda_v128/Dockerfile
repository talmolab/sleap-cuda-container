
# Base image with GPU support (runtime for smaller size)
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