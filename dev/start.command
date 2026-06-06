#!/bin/bash
echo "正在启动qm服务..."
docker-compose -f dev/docker-compose.yml down && docker-compose -f dev/docker-compose.yml up -d