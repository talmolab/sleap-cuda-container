FROM ghcr.io/talmolab/lablink-client-base-image:linux-amd64-latest

USER client
WORKDIR /home/client

RUN uv venv /home/client/.venv && \
    uv pip install --python=/home/client/.venv/bin/python sleap[nn]==1.5.2