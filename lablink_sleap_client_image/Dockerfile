# Base image with SLEAP and GPU support
# https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general
FROM ghcr.io/talmolab/sleap-cuda:linux-amd64-2a8cefd7d0291d2ce07998fa3c54c9d0d618d31b

# https://askubuntu.com/questions/1402167/must-specify-the-user-name-option-when-running-as-root-chrome-remote-desktop
# Must be a non-root user to run Chrome Remote Desktop
ARG USERNAME="client"
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages for Chrome Remote Desktop (CRD) setup
RUN apt-get update && apt-get install -y \
    # Tools for downloading files and dependencies
    curl \
    # Base packages for compatibility with GCC-10 and other software
    gcc-10-base \
    libgcc-s1 \
    # XFCE4 desktop environment for lightweight graphical interface
    xfce4 \
    desktop-base \
    # Required for session and screen management
    dbus-x11 \
    xscreensaver \
    xbase-clients \
    xvfb \
    # Python packages required by Chrome Remote Desktop
    # Handles versioning and dependency management for Python packages
    python3-packaging \
    # Provides system utilization and process management utilities
    python3-psutil \
    # Handles X Desktop Group file format support
    python3-xdg \
    # Miscellaneous dependencies
    # Provides process management utilities
    psmisc \
    # Dummy X server for headless environments
    xserver-xorg-video-dummy \
    # Supports session management and terminal multiplexers
    libutempter0 \
    # Enables secure communication and package verification
    gnupg2 \
    # Allows running commands as root
    sudo \
    # For cloning repositories and managing code
    git \
    # Clean up unnecessary files to reduce image size
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Chrome Remote Desktop
RUN  curl https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/chrome-remote-desktop.gpg && \
    # Add the Chrome Remote Desktop repository
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome-remote-desktop/deb stable main" > /etc/apt/sources.list.d/chrome-remote-desktop.list && \
    # Update package lists and install Chrome Remote Desktop
    apt-get update && apt-get install --assume-yes chrome-remote-desktop && \
    # Clean up to reduce image size
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure Chrome Remote Desktop to use Xfce by default
RUN echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session

# Because there is no display connected to your instance, disable the display manager service on your instance
RUN systemctl disable lightdm.service

# Create the user USERNAME
RUN useradd -m -s /bin/bash ${USERNAME} && echo "${USERNAME}:password" | chpasswd && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# Add USERNAME to the chrome-remote-desktop group
RUN usermod -aG chrome-remote-desktop ${USERNAME}

# Relax permissions on Python site-packages so that packages can write.
RUN chmod -R a+w /usr/local/lib/python3.8/dist-packages

# Pip install client service package
RUN python3 -m pip install lablink-client-service

# Switch to non-root user for Google Chrome Remote Desktop to work.
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Install Firefox
RUN sudo apt-get update && \
    sudo apt-get install -y firefox && \
    sudo rm -rf /var/lib/apt/lists/*

# Copy the startup script
COPY start.sh /home/${USERNAME}/start.sh
RUN sudo chmod +x /home/${USERNAME}/start.sh

# Entrypoint included since opening terminal is needed to authorize connect of the remote computer to your Google Chrome account. 
CMD ["/home/client/start.sh"]