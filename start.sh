#!/bin/bash
# ExamGenerator - Start Script (Linux/Mac)

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Starting ExamGenerator..."
echo "============================"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed.${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found.${NC}"
    if [ -f .env.example ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo -e "${GREEN}✓ .env created.${NC}"
    else
        echo -e "${RED}❌ Error: .env.example not found. Cannot create config.${NC}"
        exit 1
    fi
fi

# Start Docker Compose
echo "🐳 Lifting containers..."
docker-compose up -d app web

echo ""
echo -e "${GREEN}✅ Check complete!${NC}"
echo "-----------------------------------"
echo "🌐 Web Interface: http://localhost:5000"
echo "📋 Logs: docker-compose logs -f web"
echo "-----------------------------------"
