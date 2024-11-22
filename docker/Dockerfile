# Base image with GPU support
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# Install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get install -y --no-install-recommends python3-pip \
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
    tightvncserver \
    xfonts-base \
    xfonts-75dpi && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Install SLEAP
RUN pip install --no-cache-dir sleap[pypi]==1.3.4

# Set QT debug environment variable to help debug issues with Qt plugins
ENV QT_DEBUG_PLUGINS=1

# Needed for VNC
ENV USER=root

# Set up VNC environment
RUN mkdir -p /root/.vnc && touch /root/.Xauthority && \
    echo "password" | tightvncpasswd -f > /root/.vnc/passwd && \
    chmod 600 /root/.vnc/passwd && chmod 600 /root/.Xauthority && \
    echo "#!/bin/sh\nxrdb $HOME/.Xresources\nstartxfce4 &" > /root/.vnc/xstartup && \
    chmod +x /root/.vnc/xstartup

# Expose VNC port
EXPOSE 5901

# Automatically start VNC server and keep container running
ENTRYPOINT ["bash", "-c", "tightvncserver :1 -geometry 1920x1080 -depth 24 &>> /root/.vnc/vncserver.log && tail -f /root/.vnc/vncserver.log"]