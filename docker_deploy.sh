#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 镜像地址
IMAGE="crpi-608fba9xxjhcq7gx.cn-shanghai.personal.cr.aliyuncs.com/dcby/img2excel:latest"
CONTAINER_NAME="img2excel"

# 检查必要的环境变量
check_env_vars() {
    local missing_vars=()
    local required_vars=(
        "DASHSCOPE_API_KEY"
        "MINIO_HOST"
        "MINIO_ACCESS_KEY"
        "MINIO_SECRET_KEY"
    )

    # 首先检查 .env 文件
    if [ -f ".env" ]; then
        echo -e "${GREEN}找到 .env 文件，将使用其中的环境变量${NC}"
        return 0
    fi

    # 如果没有 .env 文件，检查环境变量
    echo -e "${YELLOW}未找到 .env 文件，检查系统环境变量...${NC}"
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo -e "${RED}错误: 缺少以下必要的环境变量:${NC}"
        printf '%s\n' "${missing_vars[@]}"
        echo -e "${YELLOW}请创建 .env 文件或设置系统环境变量${NC}"
        exit 1
    fi

    echo -e "${GREEN}所有必要的环境变量已设置${NC}"
}

# 检查 Docker 是否运行
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}错误: Docker 未运行${NC}"
        echo "请启动 Docker 后重试"
        exit 1
    fi
}

# 拉取最新镜像
pull_image() {
    echo -e "${YELLOW}拉取最新镜像...${NC}"
    if docker pull ${IMAGE}; then
        echo -e "${GREEN}镜像拉取成功${NC}"
    else
        echo -e "${RED}错误: 镜像拉取失败${NC}"
        exit 1
    fi
}

# 停止并删除旧容器
cleanup_old_container() {
    if docker ps -a | grep -q ${CONTAINER_NAME}; then
        echo -e "${YELLOW}停止并删除旧容器...${NC}"
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1
        docker rm ${CONTAINER_NAME} > /dev/null 2>&1
    fi
}

# 启动新容器
start_container() {
    echo -e "${YELLOW}启动新容器...${NC}"
    local env_args=""
    
    # 如果存在 .env 文件，使用它
    if [ -f ".env" ]; then
        env_args="--env-file .env"
    else
        # 否则，使用系统环境变量
        env_args="-e DASHSCOPE_API_KEY -e MINIO_HOST -e MINIO_ACCESS_KEY -e MINIO_SECRET_KEY"
    fi

    if docker run -d \
        --name ${CONTAINER_NAME} \
        --restart unless-stopped \
        -p 9527:9527 \
        ${env_args} \
        ${IMAGE}; then
        echo -e "${GREEN}容器启动成功${NC}"
        echo -e "${GREEN}应用访问地址: http://localhost:9527${NC}"
    else
        echo -e "${RED}错误: 容器启动失败${NC}"
        exit 1
    fi
}

# 检查容器健康状态
check_container_health() {
    echo -e "${YELLOW}等待服务启动...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:9527/_stcore/health > /dev/null; then
            echo -e "${GREEN}服务已成功启动${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    echo -e "\n${RED}错误: 服务启动超时${NC}"
    echo "请检查容器日志: docker logs ${CONTAINER_NAME}"
    return 1
}

# 显示容器日志
show_logs() {
    echo -e "${YELLOW}显示容器日志:${NC}"
    docker logs ${CONTAINER_NAME}
}

# 主函数
main() {
    echo -e "${YELLOW}开始部署 img2excel 服务${NC}"
    
    # 执行检查
    check_env_vars
    check_docker
    
    # 部署流程
    pull_image
    cleanup_old_container
    start_container
    check_container_health
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}部署完成!${NC}"
        echo -e "${GREEN}服务已在 http://localhost:9527 上运行${NC}"
    else
        show_logs
        echo -e "${RED}部署失败，请检查上述日志${NC}"
        exit 1
    fi
}

# 脚本入口
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "用法: ./docker_deploy.sh"
    echo "该脚本会自动拉取最新版本的镜像并部署"
    echo "环境变量可以通过 .env 文件或系统环境变量提供"
    exit 0
fi

main "$@"
