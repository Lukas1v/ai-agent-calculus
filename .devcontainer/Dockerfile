FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    zlib1g-dev \
    lzma-dev \
    libncursesw5-dev \
    xz-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.13 manually
RUN curl -O https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz && \
    tar xzf Python-3.13.0.tgz && \
    cd Python-3.13.0 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && rm -rf Python-3.13.0*

# Make Python 3.13 default
RUN ln -sf /usr/local/bin/python3.13 /usr/local/bin/python && \
    ln -sf /usr/local/bin/python3.13 /usr/bin/python

# Install uv (using the standalone installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

WORKDIR /workspace
