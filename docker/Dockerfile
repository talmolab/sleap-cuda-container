FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# Install dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends python3-pip \ 
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
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*
   
# Set QT debug environment variable to help debug issues with Qt plugins
ENV QT_DEBUG_PLUGINS=1

# Install SLEAP
RUN pip install --no-cache-dir sleap[pypi]==1.3.4
