FROM harbor.shmtu.edu.cn/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# DO NOT USE 12.0.0, IT IS NOT SUPPORTED BY PADDLEPADDLE

ARG VENV_NAME="pdftomd"
ARG HTTPS_PROXY

ENV VENV=$VENV_NAME
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENV DEBIAN_FRONTEN=noninteractive
ENV PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "--login", "-c"]

RUN apt-get update -y --fix-missing
RUN apt-get install -y git build-essential curl wget ffmpeg unzip git git-lfs sox libsox-dev && \
    apt-get clean && \
    git lfs install

RUN apt-get update && apt-get install -y \
    wget \
    git \
    curl \
	libgomp1 \
	libgl1 \
    libglib2.0-0 \
	&& rm -rf /var/lib/apt/lists/*
# ==================================================================
# conda install and conda forge channel as default
# ------------------------------------------------------------------
# Install miniforge
RUN https_proxy=${HTTPS_PROXY} wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O ~/miniforge.sh && \
    /bin/bash ~/miniforge.sh -b -p /opt/conda && \
    rm ~/miniforge.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo "source /opt/conda/etc/profile.d/conda.sh" >> /opt/nvidia/entrypoint.d/100.conda.sh && \
    echo "source /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate ${VENV}" >> /opt/nvidia/entrypoint.d/110.conda_default_env.sh && \
    echo "conda activate ${VENV}" >> $HOME/.bashrc

ENV PATH /opt/conda/bin:$PATH

RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict
# ------------------------------------------------------------------
# ~conda
# ==================================================================

RUN conda create -y -n ${VENV} python=3.10
ENV CONDA_DEFAULT_ENV=${VENV}
ENV PATH /opt/conda/bin:/opt/conda/envs/${VENV}/bin:$PATH

WORKDIR /app

RUN conda activate ${VENV} && conda install -y -c conda-forge pynini==2.1.5

# Install Python dependencies
COPY requirements.txt .

RUN conda activate ${VENV} && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com && \
    pip install paddlepaddle-gpu==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

COPY . .

ENV HF_HOME=./hf/

# Download MinerU models
RUN conda activate ${VENV} && HTTPS_PROXY=${HTTPS_PROXY} python download_models_hf.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
