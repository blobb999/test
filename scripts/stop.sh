#!/bin/bash

# KI Self Sustain Stop Script
set -e

echo "🛑 Stopping KI Self Sustain System..."

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${RED}[STOPPED]${NC} $1"
}

# Stop services
print_status "Stopping all services..."
docker-compose down

print_success "KI Self Sustain System stopped!"

# Optional: Remove volumes (uncomment if needed)
# echo "Removing volumes..."
# docker-compose down -v

