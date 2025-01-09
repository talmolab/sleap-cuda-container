# sleap-chrome-remote-desktop

## Description
This repo contains a DockerFile for a lightweight container (~2.79 GB) with the PyPI installation of SLEAP and all of its dependencies and a Chrome Remote Desktop server. The Chrome Remote Desktop server can be connected to using port 5901.

The base image used is [eberrigan/sleap-cuda:latest](https://hub.docker.com/layers/eberrigan/sleap-cuda/latest/images/sha256-9cc93c86cc60d0f8e357bf58c2901d9b29a509c70ae16ed90ea56ac6d33418e7?context=repo).

- The Dockerfile is located at `docker/Dockerfile`.
- The repo has CI set up in `.github/workflows` for building and pushing the image when making changes.
  - The workflow uses the linux/amd64 platform to build. 
- `.devcontainer/devcontainer.json` is convenient for developing inside a container made with the DockerFile using Visual Studio Code.
- Test data for training is located in `tests/data`.

## Installation

**Make sure to have Docker Daemon running first**


You can pull the image if you don't have it built locally, or need to update the latest, with

```bash
docker pull eberrigan/sleap-chrome-remote-desktop:latest
```

## Usage

<!-- TODO: Update after publishing the image -->

**Notes:**

- `-it` ensures that you get an interactive terminal. The `i` stands for interactive, and `t` allocates a pseudo-TTY, which is what allows you to interact with the bash shell inside the container.
- The `-v` or `--volume` option mounts the specified directory with the same level of access as the directory has on the host.
- `bash` is the command that gets executed inside the container, which in this case is to start the bash shell.
- The `--rm` flag in a docker run command automatically removes the container when it stops. This is useful for running temporary or one-time containers without cluttering your Docker environment with stopped containers.
- The `--built-args` is used to pass build-time variables to the Dockerfile. In this case, the `USERNAME` variable is set to `tutorial` as default but able to be changed when building the image.

To build the image locally, run

```
docker build -t sleap-chrome-remote-desktop .
```

Then, to run the image with gpus interactively and mapping port 5901, which is exposed in the container, to port 5901 on a VNC client

```
docker run --rm -it --gpu=all sleap-chrome-remote-desktop
```

# Connecting to the Chrome Remote Desktop

This guide explains how to connect to the Chrome Remote Desktop server running in the container to access the graphical user interface (GUI).

## Prerequisites

1. **Google Account**: You need a Google account to use Chrome Remote Desktop.
2. **Chrome Browser**: You need to have the Chrome browser installed on your local machine.
3. **Docker Setup**: 
   - Ensure Docker is installed on your local machine.

## Steps to Connect to the Chrome Remote Desktop

### 1. Start the Docker Container

Start the Docker container with the Chrome Remote Desktop server running in it.

```bash
docker run --rm -it --gpus=all <your-container-name> bash
```

### 2. Connect to the Chrome Remote Desktop

1. Go to [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access) in your Chrome browser.

2. Sign in with your Google account.

3. Then, click "Set up via SSH" on the left and follow the provided steps.
- This will provide the command in this form: 
  ```bash
  DISPLAY= /opt/google/chrome-remote-desktop/start-host \
    --code="4/xxxxxxxxxxxxxxxxxxxxxxxx" \
    --redirect-url="https://remotedesktop.google.com/_/oauthredirect" \
    --name=$(hostname)
  ```

1. Run the provided command in your terminal with Docker container running.

2. When prompted, enter 6-digit PIN. This number will be used for additional authorization when you connect later.

### 3. Run Chrome Remote Desktop

1. Go to [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access) in your Chrome browser.

2. Sign in with your Google account.

3. Then, click "Remote Access" to check the status of your remote desktop (make sure to refresh the page).

4. If you see the status as "Online", click on the remote desktop to connect and enter the 6-digit PIN you set earlier.

### 4. Access the GUI

Once connected, you'll see the desktop environment configured in the container. You can now open and use GUI-based applications such as `sleap-label`.

## Troubleshooting

1. **Cannot Access GUI with User due to Permission Errors:**
   - Change the user to `root` in the Dockerfile to avoid permission issues with command: 
```bash
  sudo su
```

## Support
contact Elizabeth at eberrigan@salk.edu