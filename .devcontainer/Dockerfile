FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# ── Base tools + Python ───────────────────────────────────────────────────────
# Ubuntu 24.04 ships Python 3.12 in main — no PPA needed.
# Production containers use python:3.13-alpine; the project requires >=3.10
# so 3.12 here is intentional: we get a stable, natively packaged interpreter
# without the deadsnakes-PPA arm64 gap (3.13 isn't built for arm64 there yet).
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        gnupg \
        iproute2 \
        jq \
        make \
        nano \
        python3.12 \
        python3.12-dev \
        python3.12-venv \
        python3-pip \
        software-properties-common \
        sudo \
        vim \
        wget \
    && update-alternatives --install /usr/bin/python  python  /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /usr/lib/python3.12/EXTERNALLY-MANAGED

# ── Docker CLI (no daemon — host socket is mounted at runtime) ─────────────────
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /usr/share/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] \
        https://download.docker.com/linux/ubuntu noble stable" \
        > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# ── Non-root user ─────────────────────────────────────────────────────────────
# Ubuntu 24.04 ships an "ubuntu" user at UID/GID 1000. Rename it instead
# of creating a fresh group to avoid the "GID already exists" error.
ARG USERNAME=dev

RUN groupmod -n $USERNAME ubuntu \
    && usermod -l $USERNAME -d /home/$USERNAME -m -s /bin/bash ubuntu \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ── Shell config ──────────────────────────────────────────────────────────────
COPY bashrc.sh /etc/profile.d/devcontainer_ps1.sh
RUN echo 'source /etc/profile.d/devcontainer_ps1.sh' >> /home/$USERNAME/.bashrc

USER $USERNAME
WORKDIR /workspace/sample_code_1
