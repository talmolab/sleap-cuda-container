# Base image with SLEAP and GPU support
# https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general
FROM eberrigan/sleap-cuda:latest

# Install required tools for VNC server
RUN apt-get update && apt-get install -y --no-install-recommends --fix-broken \    
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    xfonts-base \
    autocutsel \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends --fix-broken\
    '^libxcb.*-dev' \
    libx11-xcb-dev \
    libglu1-mesa-dev \
    libxrender-dev \
    libxi-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    desktop-base \
    xscreensaver \
    xvfb \
    xserver-xorg-video-dummy \
    x11-xserver-utils \
    x11-apps \
    at-spi2-core \
    xbase-clients && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

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