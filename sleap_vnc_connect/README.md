# sleap-vnc-connect

The SLEAP GUI will not open in the VNC server and I do not know why! VNC connection works. Something with the X server.

## Description
This repo contains a DockerFile for a lightweight container (~2.79 GB) with the PyPI installation of SLEAP and all of its dependencies and a VNC server. The VNC server can be connected to using port 5901. 
The container repository is located at [https://hub.docker.com/repository/docker/eberrigan/sleap-vnc-connect/general](https://hub.docker.com/repository/docker/eberrigan/sleap-vnc-connect/general). 

The base image used is [nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04](https://hub.docker.com/layers/nvidia/cuda/11.3.1-cudnn8-runtime-ubuntu20.04/images/sha256-025a321d3131b688f4ac09d80e9af6221f2d1568b4f9ea6e45a698beebb439c0).
- The Dockerfile is located at `docker/Dockerfile`.
- The repo has CI set up in `.github/workflows` for building and pushing the image when making changes.
  - The workflow uses the linux/amd64 platform to build. 
- `.devcontainer/devcontainer.json` is convenient for developing inside a container made with the DockerFile using Visual Studio Code.
- Test data for training is located in `tests/data`.


## Installation

**Make sure to have Docker Daemon running first**


You can pull the image if you don't have it built locally, or need to update the latest, with

```
docker pull eberrigan/sleap-vnc-connect:latest
```

## Usage 

Then, to run the image with gpus interactively and mapping port 5901, which is exposed in the container, to port 5901 on a VNC client

```
docker run --gpus all -it -p 5901:5901 eberrigan/sleap-vnc-connect:latest bash
```

and test with 

```
python -c "import sleap; sleap.versions()" && nvidia-smi
```

In general, use the syntax

```
docker run -v /path/on/host:/path/in/container [other options] image_name [command]
```

Note that host paths are absolute. 


Use this syntax to give host permissions to mounted volumes
```
docker run -u $(id -u):$(id -g) -v /your/host/directory:/container/directory [options] your-image-name [command]
```

```
docker run -u $(id -u):$(id -g) -v ./tests/data:/workspace/tests/data --gpus all -it -p 5901:5901 eberrigan/sleap-vnc-connect:latest bash
```

Test:

```
 python3 -c "import sleap; print('SLEAP version:', sleap.__version__)"
 nvidia-smi # Check that the GPUs are disvoerable
 ps aux | grep Xtightvnc # Check that the VNC server is running
 echo $DISPLAY # Check display environment variable is :1
 sleap-train "tests/data/initial_config.json" "tests/data/dance.mp4.labels.slp" --video-paths "tests/data/dance.mp4"
```

**Notes:**

- The `eberrigan/sleap-vnc-connect` is the Docker registry where the images are pulled from. This is only used when pulling images from the cloud, and not necesary when building/running locally.
- `-it` ensures that you get an interactive terminal. The `i` stands for interactive, and `t` allocates a pseudo-TTY, which is what allows you to interact with the bash shell inside the container.
- The `-v` or `--volume` option mounts the specified directory with the same level of access as the directory has on the host.
- `bash` is the command that gets executed inside the container, which in this case is to start the bash shell.
- `p` The -p 5901:5901 flag in a Docker run command maps a port on the host machine to a port inside the container. 

```
-p [host-port]:[container-port]
```

`host-port`: The port number on the host machine (your local computer or server).
`container-port`: The port number inside the Docker container.
In this case, 5901 is mapped both inside and outside the container.

- Order of operations is 1. Pull (if needed): Get a pre-built image from a registry. 2. Run: Start a container from an image.

## Contributing

- Use the `devcontainer.json` to open the folder `sleap_vnc_connect` in a dev container using VS Code.
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

```
docker pull eberrigan/sleap-vnc-connect:linux-amd64-test
```

then 

```
docker run -v ./tests/data:/workspace/tests/data --gpus all -p 5901:5901 -it eberrigan/sleap-vnc-connect:linux-amd64-test bash
```

To build locally for testing you can use the command:

```
docker build --platform linux/amd64 .
```

## Support
contact Elizabeth at eberrigan@salk.edu
