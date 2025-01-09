#!/bin/bash

# 检查是否提供了版本参数
if [ -z "$1" ]; then
    echo "Error: Version parameter is required"
    echo "Usage: ./local_build_image.sh <version>"
    exit 1
fi

VERSION=$1
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
IMAGE_NAME="registry.cn-hangzhou.aliyuncs.com/img2excel/expense-report"

# 构建镜像
echo "Building Docker image with version: $VERSION"
docker build -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest .

# 保存镜像到 dist 目录
echo "Saving Docker image to dist/img2excel-${TIMESTAMP}.tar.gz"
mkdir -p dist
docker save ${IMAGE_NAME}:${VERSION} | gzip > dist/img2excel-${TIMESTAMP}.tar.gz

echo "Done! Image has been built and saved."
echo "You can run the image using:"
echo "docker run -p 8501:8501 --env-file .env ${IMAGE_NAME}:${VERSION}"
