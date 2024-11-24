# Base image with GPU support
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

ENV USER=root

# Install dependencies
# opencv requires opengl https://github.com/conda-forge/opencv-feedstock/issues/401
# https://medium.com/@gustav0.lewin/how-to-make-a-docker-container-with-vnc-access-f607958141ae
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
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    xfonts-base \
    x11-xserver-utils \
    x11-utils \
    autocutsel \
    python3-pip && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install SLEAP
RUN pip install --no-cache-dir sleap[pypi]==1.3.4

ENV NVIDIA_DRIVER_CAPABILITIES=all

# Set QT debug environment variable to help debug issues with Qt plugins
ENV QT_DEBUG_PLUGINS=1

# Setup VNC server
RUN mkdir /root/.vnc && \
    echo "password" | vncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd

# Create an .Xauthority file
RUN touch /root/.Xauthority

# Set display resolution (change as needed)
ENV RESOLUTION=1920x1080

# Expose VNC port
EXPOSE 5901

# Set the working directory in the container
WORKDIR /app

# Copy a script to start the VNC server
COPY start-vnc.sh start-vnc.sh
RUN chmod +x start-vnc.sh

# Start the VNC server
ENTRYPOINT ["/app/start-vnc.sh"]