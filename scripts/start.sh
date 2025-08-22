#!/bin/bash

# KI Self Sustain Start Script
set -e

echo "🚀 Starting KI Self Sustain System..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if docker-compose.yml exists
if [ ! -f docker-compose.yaml ]; then
    echo "Error: docker-compose.yaml not found!"
    exit 1
fi

# Start services
print_status "Starting all services..."
docker-compose up -d

# Wait for services
print_status "Waiting for services to initialize..."
sleep 15

# Show status
print_status "Service status:"
docker-compose ps

print_success "KI Self Sustain System started!"
echo ""
echo "Access the system at: http://localhost"
echo "View logs with: docker-compose logs -f"
echo "Stop with: docker-compose down"

