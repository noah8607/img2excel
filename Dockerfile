FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖并清理
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt && \
    find /usr/local -type d -name __pycache__ -exec rm -rf {} + && \
    rm -rf /root/.cache

# 复制应用代码
COPY utils/ ./utils/
COPY streamlit_app.py .
COPY LICENSE .
COPY README.md .

# 暴露端口
EXPOSE 9527

# 启动命令
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=9527", "--server.address=0.0.0.0"]
