#!/bin/bash

echo "Stopping all running containers..."
docker stop $(docker ps -aq)

echo "Removing all containers..."
docker rm $(docker ps -aq)

# echo "Removing all images..."
# docker rmi $(docker images -q)

echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

echo "Removing all networks..."
docker network prune -f

echo "Performing a system prune to remove all unused data..."
docker system prune -a --volumes -f

echo "Docker cleanup complete!"