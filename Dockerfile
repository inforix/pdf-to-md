FROM python:3.10-slim

ARG HTTPS_PROXY

ENV https_proxy=${HTTPS_PROXY}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    curl \
	libgomp1 \
	libgl1 \
    libglib2.0-0 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configure pip to use Tsinghua mirror
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com

COPY . .

# Download MinerU models
RUN HF_ENDPOINT=https://hf-mirror.com python download_models_hf.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 