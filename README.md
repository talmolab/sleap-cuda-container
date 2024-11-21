# sleap-train


## Description
This repo contains a DockerFile for a lightweight container (~3.23 GB) with the PyPI installation of SLEAP and all of its dependencies, including [TensorFlow 2.7.0](https://hub.docker.com/layers/tensorflow/tensorflow/2.7.0-gpu/images/sha256-fc5eb0604722c7bef7b499bb007b3050c4beec5859c2e0d4409d2cca5c14d442?context=explore) as a base image with expected ARCH x86_64. The container registry is located at [https://gitlab.com/salk-tm/sleap-train/container_registry/6343604](https://gitlab.com/salk-tm/sleap-train/container_registry/6343604).

- "./src/" contains a logging utility file which is convenient for logging everything to a text file.
- The repo has CI set up in ".gitlab-ci.yml" for testing the DockerFile when making changes.
- ".devcontainer\devcontainer.json" is convenient for developing inside a container made with the DockerFile using Visual Studio Code.
- Test data for training is located in "tests\data".



## Badges
[![pipeline status](https://gitlab.com/salk-tm/sleap-train/badges/main/pipeline.svg)](https://gitlab.com/salk-tm/sleap-train/-/commits/main)

[![coverage report](https://gitlab.com/salk-tm/sleap-train/badges/main/coverage.svg)](https://gitlab.com/salk-tm/sleap-train/-/commits/main)

## Installation

**Make sure to have Docker Desktop running first**


You can pull the image if you don't have it built locally, or need to update the latest, with

```
docker pull registry.gitlab.com/salk-tm/sleap-train:latest
```

## Usage 

Then, to run the image with gpus interactively:

```
docker run --gpus all -it registry.gitlab.com/salk-tm/sleap-train:latest bash
```

and test with 

```
python -c "import sleap; sleap.versions()" && nvidia-smi
```

To run the image interactively with data mounted to the container, use the syntax

```
docker run -v /path/on/host:/path/in/container [other options] image_name [command]
```

Note that host paths are absolute. 


Use this syntax to give host permissions to mounted volumes
```
docker run -u $(id -u):$(id -g) -v /your/host/directory:/container/directory [options] your-image-name [command]
```

```
docker run -u $(id -u):$(id -g) -v ./tests/data:/workspace/tests/data --gpus all -it registry.gitlab.com/salk-tm/sleap-train:latest bash
```

Test:

```
 python -c "import sleap; print('SLEAP version:', sleap.__version__)"
 sleap-train "tests/data/initial_config.json" "tests/data/dance.mp4.labels.slp" --video-paths "tests/data/dance.mp4"
```

## Contributing

- Use the `devcontainer.json` to open the repo in a dev container using VS Code.
  - There is some test data in the `tests` directory that will be automatically mounted for use since the working directory is the workspace.
  - Rebuild the container when you make changes using `Dev Container: Rebuild Container`.

- Please make a new branch, starting with your name, with any changes, and request a reviewer before merging with the main branch since this container will be used by all HPI.
- Please document using the same conventions (docstrings for each function and class, typing-hints, informative comments).
- Tests are written in the pytest framework. Data used in the tests are defined as fixtures in "tests/fixtures/data.py" ("https://docs.pytest.org/en/6.2.x/reference.html#fixtures-api").

**Notes:**

- The `registry.gitlab.com` is the Docker registry where the images are pulled from. This is only used when pulling images from the cloud, and not necesary when building/running locally.
- `-it` ensures that you get an interactive terminal. The `i` stands for interactive, and `t` allocates a pseudo-TTY, which is what allows you to interact with the bash shell inside the container.
- The `-v` or `--volume` option mounts the specified directory with the same level of access as the directory has on the host.
- `bash` is the command that gets executed inside the container, which in this case is to start the bash shell.
- Order of operations is 1. Pull (if needed): Get a pre-built image from a registry. 2. Run: Start a container from an image.


## Build
To build via automated CI, just push to `main`. See [`.gitlab-ci.yml`](.gitlab-ci.yml) for the runner definition.

To build locally for testing:

```
docker build --platform linux/amd64 --tag registry.gitlab.com/salk-tm/sleap-train:latest .
```

## Support
contact Elizabeth at eberrigan@salk.edu
