# sleap-cuda

## Description

This repo contains a DockerFile for a lightweight container (~19.7 GB) with the PyPI installation of SLEAP v1.5.1 and all of its dependencies. The container repository is located at [https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general](https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general).

The base image used is [ghcr.io/talmolab/sleap-nn-cuda](https://github.com/talmolab/sleap-nn-cuda/pkgs/container/sleap-nn-cuda).

- The Dockerfile is located at `docker/Dockerfile`.
- The repo has CI set up in `.github/workflows` for building and pushing the image when making changes.
  - The workflow uses the linux/amd64 platform to build.
- `.devcontainer/devcontainer.json` is convenient for developing inside a container made with the DockerFile using Visual Studio Code.
- Test data for training is located in `tests/data`.

## Installation

**Make sure to have Docker Daemon running first**

You can pull the image if you don't have it built locally, or need to update the latest, with

```
docker pull ghcr.io/talmolab/sleap-v151-cuda:latest
```

## Usage

Then, to run the image with gpus interactively:

```
docker run --gpus all -it ghcr.io/talmolab/sleap-v151-cuda:latest bash
```

and test with

```
uv run python -c "import sleap; sleap.versions()" && nvidia-smi
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
docker run -u $(id -u):$(id -g) -v ./tests/data:/tests/data --gpus all -it ghcr.io/talmolab/sleap-v151-cuda:latest bash
```

Test:

```
 uv run python -c "import sleap; print('SLEAP version:', sleap.__version__)"
 nvidia-smi # Check that the GPUs are discoverable
 uv run sleap-train "tests/data/initial_config.json" "tests/data/dance.mp4.labels.slp" --video-paths "tests/data/dance.mp4"
```

**Notes:**

- The `ghcr.io/talmolab/sleap-v151-cuda` is the Docker registry where the images are pulled from. This is only used when pulling images from the cloud, and not necesary when building/running locally.
- `-it` ensures that you get an interactive terminal. The `i` stands for interactive, and `t` allocates a pseudo-TTY, which is what allows you to interact with the bash shell inside the container.
- The `-v` or `--volume` option mounts the specified directory with the same level of access as the directory has on the host.
- `bash` is the command that gets executed inside the container, which in this case is to start the bash shell.
- Order of operations is 1. Pull (if needed): Get a pre-built image from a registry. 2. Run: Start a container from an image.

## Contributing

- Use the `devcontainer.json` to open the repo in a dev container using VS Code.

  - There is some test data in the `tests` directory that will be automatically mounted for use since the working directory is the workspace.
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
docker pull ghcr.io/talmolab/sleap-v151-cuda:linux-amd64-test
```

then

```
docker run -v ./tests/data:/tests/data --gpus all -it ghcr.io/talmolab/sleap-v151-cuda:linux-amd64-test bash
```

To build locally for testing you can use the command (from the root of the repo):

```
docker build --platform linux/amd64 ./sleap_v151_cuda_v128
```

## Support

contact Elizabeth at eberrigan@salk.edu
