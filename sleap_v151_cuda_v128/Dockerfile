# Base image with GPU support
FROM ghcr.io/talmolab/sleap-nn-cuda:linux-amd64-test

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

# Install sleap-nn w/ CUDA 12.8 support
RUN uv add sleap[nn] --index https://download.pytorch.org/whl/cu128 --index https://pypi.org/simple --no-cache