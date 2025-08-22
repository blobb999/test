#!/bin/bash

# KI Self Sustain Setup Script
set -e

echo "🚀 Setting up KI Self Sustain System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose are available"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs backups flowise_data llm_models redis_data
mkdir -p monitoring/prometheus_data monitoring/grafana_data
mkdir -p dev_scripts

print_success "Directories created"

# Set permissions
print_status "Setting permissions..."
chmod +x scripts/*.sh
chmod 755 data logs backups flowise_data llm_models redis_data
chmod 755 monitoring/prometheus_data monitoring/grafana_data

print_success "Permissions set"

# Copy environment file if it doesn't exist
if [ ! -f .env.local ]; then
    print_status "Creating local environment file..."
    cp .env .env.local
    print_warning "Please review and modify .env.local as needed"
fi

# Build and start services
print_status "Building Docker images..."
docker-compose build --no-cache

print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 30

# Check service health
print_status "Checking service health..."

# Check backend
if curl -f http://localhost:5000/api/ai/status &> /dev/null; then
    print_success "Backend service is healthy"
else
    print_warning "Backend service may not be ready yet"
fi

# Check frontend
if curl -f http://localhost/ &> /dev/null; then
    print_success "Frontend service is healthy"
else
    print_warning "Frontend service may not be ready yet"
fi

# Check Flowise
if curl -f http://localhost:3000 &> /dev/null; then
    print_success "Flowise service is healthy"
else
    print_warning "Flowise service may not be ready yet"
fi

# Setup LLM model
print_status "Setting up LLM model..."
docker-compose exec -T llm_service ollama pull llama3 || print_warning "Failed to pull LLM model"

print_success "Setup completed!"

echo ""
echo "🎉 KI Self Sustain System is ready!"
echo ""
echo "Access points:"
echo "  • Frontend (GUI): http://localhost"
echo "  • Backend API: http://localhost:5000"
echo "  • Flowise: http://localhost:3000 (admin/ki_self_sustain_2024)"
echo "  • LLM Service: http://localhost:11434"
echo "  • Prometheus: http://localhost:9090"
echo "  • Grafana: http://localhost:3001 (admin/ki_self_sustain_2024)"
echo ""
echo "To stop the system: docker-compose down"
echo "To view logs: docker-compose logs -f"
echo "To restart: docker-compose restart"
echo ""
print_success "Happy AI controlling! 🤖"

