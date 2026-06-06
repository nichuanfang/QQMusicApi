#!/bin/bash
echo "正在启动qm服务..."
docker-compose -f dev/docker-compose.yml restart && docker logs -f qm