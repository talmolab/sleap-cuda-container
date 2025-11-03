FROM ghcr.io/talmolab/lablink-client-base-image:linux-amd64-latest

USER client
WORKDIR /home/client

ARG PACKAGE_VERSION=0.0.8a0

# Since sleap requires python >=3.11, we need to create a new venv with that version
# and install both sleap and lablink-client-service into that venv.
RUN uv python install 3.11 \
 && rm -rf /home/client/.venv \
 && uv venv --python="$(uv python find 3.11)" /home/client/.venv \
 && uv pip install --python=/home/client/.venv/bin/python \
      "lablink-client-service==${PACKAGE_VERSION}" \
 && uv pip install --python=/home/client/.venv/bin/python \
      'sleap[nn]==1.5.2' \
      --index https://download.pytorch.org/whl/cu128 \
      --index https://pypi.org/simple