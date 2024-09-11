# 第一阶段：使用 Python 镜像安装 Python 和需要的 Python 包
FROM python:slim AS python-base
RUN pip install uv

# 第二阶段：使用 texlive 镜像，并安装 git，然后从第一阶段复制 Python
FROM texlive/texlive:latest

# 从第一阶段复制 Python 和它的库
COPY --from=python-base /usr/local /usr/local

WORKDIR /app
COPY requirements.lock ./
RUN uv pip install --no-cache --system -r requirements.lock

COPY src .
ENTRYPOINT ["python", "main.py"]
CMD []
