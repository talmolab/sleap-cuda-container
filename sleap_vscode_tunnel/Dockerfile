# Base image with SLEAP and GPU support
# https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general
FROM eberrigan/sleap-cuda:latest

# Install VS Code CLI
RUN curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz && \
    tar -xf vscode_cli.tar.gz -C /usr/local/bin && \
    rm vscode_cli.tar.gz

# Add VS Code CLI to PATH
ENV PATH="/usr/local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Add a script to run the VS Code tunnel
# https://code.visualstudio.com/docs/remote/tunnels#_using-the-code-cli
RUN echo "#!/bin/bash\n\n# Start VS Code tunnel\ncode tunnel --accept-server-license-terms" > /app/start-tunnel.sh && \
    chmod +x /app/start-tunnel.sh

# Start VS Code tunnel
ENTRYPOINT ["/app/start-tunnel.sh"]