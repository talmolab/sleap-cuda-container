# sleap-chrome-remote-desktop

## Description
This folder of the repo contains a DockerFile for a lightweight container (~9.75 GB) with the PyPI installation of SLEAP and all of its dependencies and a Chrome Remote Desktop server.

The base image used is [eberrigan/sleap-cuda:latest](https://hub.docker.com/layers/eberrigan/sleap-cuda/latest/images/sha256-9cc93c86cc60d0f8e357bf58c2901d9b29a509c70ae16ed90ea56ac6d33418e7?context=repo).

- The Dockerfile is located at `./sleap_chrome_remote_desktop/Dockerfile`.
- The repo has CI set up in `.github/workflows` for building and pushing the image when making changes.
  - The workflow uses the linux/amd64 platform to build. 
- `./sleap_chrome_remote_desktop/.devcontainer/devcontainer.json` is convenient for developing inside a container made with the DockerFile using Visual Studio Code.
- Test data for training is located in `./tests/data`.

## Installation

**Make sure to have Docker Daemon running first**


You can pull the image if you don't have it built locally, or need to update the latest, with

```bash
docker pull eberrigan/sleap-chrome-remote-desktop:latest
```

## Usage

Then, to run the image with GPUs interactively,

``` bash
docker run --gpus all -it eberrigan sleap-chrome-remote-desktop:latest
```

and test with

```bash
python3 -c "import sleap; sleap.versions()" && nvidia-smi
```

In general, use the syntax: 

```bash
docker run -v /path/on/host:/path/in/container [other options] image_name [command]
```

**Notes:**

- `-it` ensures that you get an interactive terminal. The `i` stands for interactive, and `t` allocates a pseudo-TTY, which is what allows you to interact with the bash shell inside the container.
- The `-v` or `--volume` option mounts the specified directory with the same level of access as the directory has on the host.
- The `--rm` flag in a docker run command automatically removes the container when it stops. This is useful for running temporary or one-time containers without cluttering your Docker environment with stopped containers.

To build the image locally, run

```bash
docker build -t sleap-chrome-remote-desktop .
```

Then, to run the image with gpus interactively

```bash
docker run --rm -it --gpus=all sleap-chrome-remote-desktop
```

# Connecting to the Chrome Remote Desktop

This guide explains how to connect to the Chrome Remote Desktop server running in the container to access SLEAP installed in the container, including the SLEAP GUI.

## Prerequisites

1. **Google Account**: You need a Google account to use Chrome Remote Desktop.
2. **Chrome Browser**: You need to have the Chrome browser installed on your local machine.
3. **Docker Setup**: 
   - Ensure Docker is installed and running on your system.

## Steps to Connect to the Chrome Remote Desktop

### 1. Start the Docker Container

Start the Docker container with the Chrome Remote Desktop server running in it.

```bash
docker run --rm -it --gpus=all <your-container-name>
```

### 2. Connect to the Chrome Remote Desktop

1. On your local machine, go to [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access) in your Chrome browser.

2. Sign in with your Google account.

3. Then, click "Set up via SSH" on the left and follow the provided steps.
- This will provide the command in this form: 
  ```bash
  DISPLAY= /opt/google/chrome-remote-desktop/start-host \
    --code="4/xxxxxxxxxxxxxxxxxxxxxxxx" \
    --redirect-url="https://remotedesktop.google.com/_/oauthredirect" \
    --name=$(hostname)
  ```

1. Run the provided command in your remote machine's terminal with Docker container running. Make sure to refresh the website. 

2. When prompted, enter 6-digit PIN. This number will be used for additional authorization when you connect later.

### 3. Run Chrome Remote Desktop

1. Go to [https://remotedesktop.google.com/access](https://remotedesktop.google.com/access) in your Chrome browser.

2. Sign in with your Google account.

3. Then, click "Remote Access" to check the status of your remote desktop (make sure to refresh the page).

4. If you see the status as "Online", click on the remote desktop to connect and enter the 6-digit PIN you set earlier.

### 4. Access the GUI

Once connected to the remote machine, open a terminal and use SLEAP commands like `sleap-label`. The GUI should be displayed in your chrome remote desktop display environment on your local machine.

## Contributing
- Use the `devcontainer.json` to open the folder `sleap_chrome_remote_desktop` in a dev container using VS Code.

  - Rebuild the container when you make changes using `Dev Container: Rebuild Container`.

- Please make a new branch, starting with your name, with any changes, and request a reviewer before merging with the main branch since this image will be used by others.

- Please document using the same conventions (docstrings for each function and class, typing-hints, informative comments).

- Tests are written in the pytest framework. Data used in the tests are defined as fixtures in `tests/fixtures/data.py` (https://docs.pytest.org/en/6.2.x/reference.html#fixtures-api).

## Build
To build and push via automated CI, just push changes to a branch.

- Pushes to `main` result in an image with the tag `latest`.
- Pushes to other branches have tags with `-test` appended.
- See `.github/workflows` for testing and production workflows.

To test `test` images locally use after pushing the `test` images via CI:

```bash
docker pull eberrigan/sleap-chrome-remote-desktop:linux-amd64-test
```

then

```bash
docker run -v ./tests/data:/workspace/tests/data --gpus all -it eberrigan/sleap-chrome-remote-desktop:linux-amd64-test
```

To build locally for testing you can use the command:
```bash
docker build --no-cache -t sleap-crd ./sleap_chrome_remote_desktop
docker run --gpus all -it --rm --name sleap-crd sleap-crd
```

## Support
contact Elizabeth at eberrigan@salk.edu