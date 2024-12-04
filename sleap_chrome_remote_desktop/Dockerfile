# Base image with SLEAP and GPU support
# https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general
FROM eberrigan/sleap-cuda:latest

# Install necessary packages for Chrome Remote Desktop
# psmisc and python3-psutil and python3-packaging and python3-xdg and libutempter0 for GCRD to work
RUN apt-get update && apt-get install -y \
    curl \
    gcc-10-base \
    libgcc-s1 \
    xfce4 \
    desktop-base \
    dbus-x11 \
    xscreensaver \
    xbase-clients \
    xvfb \
    python3-packaging \
    python3-psutil \
    psmisc \
    xserver-xorg-video-dummy \
    python3-xdg \ 
    libutempter0 \
    gnupg2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

# Install Google Chrome Remote Desktop
# RUN wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
# RUN dpkg --install chrome-remote-desktop_current_amd64.deb

RUN  curl https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/chrome-remote-desktop.gpg && \
    # Add the Chrome Remote Desktop repository
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome-remote-desktop/deb stable main" > /etc/apt/sources.list.d/chrome-remote-desktop.list && \
    # Update package lists and install Chrome Remote Desktop
    apt-get update && apt-get install --assume-yes chrome-remote-desktop && \
    # Clean up to reduce image size
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session

RUN systemctl disable lightdm.service

# Create the user hep003
RUN useradd -m -s /bin/bash hep003 && echo "hep003:password" | chpasswd && \
    echo "hep003 ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/hep003 && \
    chmod 0440 /etc/sudoers.d/hep003 && \
    chown -R hep003:hep003 /home/hep003

# Add hep003 to the chrome-remote-desktop group
RUN usermod -aG chrome-remote-desktop hep003

# Set up Chrome Remote Desktop for the user
USER hep003
WORKDIR /home/hep003
