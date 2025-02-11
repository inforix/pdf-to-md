# PDF to Markdown service

This project is to build a FastAPI server to handle request for converting PDF to markdown content.

## Installation

```shell
pip install -r requirements.txt
```

### Note

If you want to use GPU, please modify `device-mode` to `gpu` in `magic-pdf.template.json`:

```json
"device-mode":"cuda",
```

## Build image

If you need proxy, then specify the `--build-arg`, or just ignore it.

```shell
sudo docker compose build --build-arg HTTPS_PROXY=xxxx
```
