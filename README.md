# SLEAP CUDA Container Repository

This repository provides multiple Docker configurations for running **SLEAP** (a machine learning-based tool for animal pose estimation) in different environments, leveraging GPU support and Ubuntu. These configurations enable different ways to interact with the containerized SLEAP environment, including VNC and VS Code Tunnels.

---

## Repository Structure

The repository is organized as follows:

```
sleap-cuda-container (repo)
│
├── .github
├── sleap_cuda
│   ├── README.md
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .devcontainer
│
├── sleap_vnc_connect
│   ├── README.md
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .devcontainer
│
├── sleap_vscode_tunnel
│   ├── README.md
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .devcontainer
│
├── sleap_chrome_remote_desktop
│   ├── README.md
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .devcontainer
│
├── sleap_webRTC
|   ├── webRTC_external
│       ├── client.py
│       ├── server.py
│       ├── env.yaml
│       ├── startup.sh
|   ├── webRTC_worker_container
│       ├── Dockerfile
│       ├── worker.py
│       ├── .dockerignore
│       ├── .devcontainer
│   ├── README.md
│   
├── tests
├── README.md
├── .gitignore
└── LICENSE
```

### Subfolders and Containers

- **`sleap_cuda/`**: 
  - Contains the base image for SLEAP with GPU support and Ubuntu. 
  - This image is the foundation for other container configurations.
  - **[Docker Hub Link](https://hub.docker.com/repository/docker/eberrigan/sleap-cuda/general)**.

- **`sleap_vnc_connect/`**:
  - Adds a **VNC server** to the base image, allowing you to connect to the container using a local VNC client.
  - Useful for graphical interaction with the SLEAP GUI.
  - See the `README.md` in this folder for setup and connection instructions.

- **`sleap_vscode_tunnel/`**:
  - Adds the **VS Code CLI** for establishing a remote tunnel connection to the container.
  - Enables headless interaction with the container through VS Code.
  - Note: **VS Code Tunnels do not yet support port forwarding**, so graphical applications (like the SLEAP GUI) cannot be used with this container.

- **`sleap_chrome_remote_desktop/`**:
  - Adds **Chrome Remote Desktop** to the base image, allowing you to connect to the container's GUI using a Chrome browser.
  - See the `README.md` in this folder for setup and connection instructions.
    
- **`sleap_webRTC/`**:
  - Adds a **Worker** to the base image, allowing a client to send commands to the container's GUI and maintain connection via webRTC.
  - See the `README.md` in this folder for setup and connection instructions.

- **`tests/`**:
  - Contains test scripts for validating the functionality of the Docker configurations.

---

## Running the Containers

### 1. **Base SLEAP CUDA Container**
To use the base container:
```bash
docker pull eberrigan/sleap-cuda:latest
```

### 2. **SLEAP VNC Connect**
The `sleap_vnc_connect` container starts a **VNC server**, enabling a graphical interface for SLEAP. 

1. **Build and Run**:
   ```bash
   docker build -t sleap-vnc ./sleap_vnc_connect
   docker run --rm -it -p 5901:5901 --gpus all sleap-vnc
   ```

2. **Connect to the VNC Server**:
   - Use a VNC client and connect to `localhost:5901`.
   - Ensure your display environment variables are correctly set.

### 3. **SLEAP VS Code Tunnel**
The `sleap_vscode_tunnel` container allows **remote development** using VS Code tunnels.

1. **Build and Run**:
   ```bash
   docker build -t sleap-tunnel ./sleap_vscode_tunnel
   docker run --rm -it --gpus all sleap-tunnel
   ```

2. **Connect to the Tunnel**:
   - The VS Code CLI in the container starts a tunnel.
   - Use the provided tunnel URL in VS Code to connect and work remotely.

---

## Notes and Limitations

- **Remote Tunnels**:
  - VS Code Remote Tunnels do not currently support port forwarding. As a result, graphical applications like the SLEAP GUI cannot run in this container.

- **VNC**:
  - The VNC Connect container requires port `5901` to be exposed. Use the `-p` flag to map this port when running the container.

- **X11 Forwarding**:
  - If graphical interaction is required over an SSH connection, ensure proper X11 forwarding is set up.

---

## License
This repository is licensed under the **MIT License**. See the `LICENSE` file for more details.

For additional questions or issues, please open an issue in this repository.
