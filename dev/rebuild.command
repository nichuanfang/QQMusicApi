#!/bin/bash
echo "正在重新构建镜像并启动qm服务..."
docker-compose -f dev/docker-compose.yml down && docker-compose -f dev/docker-compose.yml up -d && docker logs -f qm