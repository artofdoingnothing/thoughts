#!/bin/bash

# Default environment variables for local development
export REDIS_HOST=localhost
export REDIS_PORT=6379
export DATABASE_URL=postgresql://user:password@localhost:5432/thoughts
export QUEUES=distortions,sentiment,generation,essay,action_orientation,thought_type,topics

# Load .env if exists
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

cleanup() {
    echo "Stopping local services..."
    [ -n "$BACKEND_PID" ] && kill $BACKEND_PID 2>/dev/null
    [ -n "$WORKER_PID" ] && kill $WORKER_PID 2>/dev/null
    [ -n "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null
    exit 0
}

while true; do
    echo "======================================"
    echo "       Thought Aggregator Menu        "
    echo "======================================"
    echo "1. Start Infrastructure (Postgres/Redis) via Docker"
    echo "2. Start All Services via Docker"
    echo "3. Start Services Locally (Backend + Workers + Frontend)"
    echo "4. Stop All Docker Services"
    echo "5. Exit"
    echo "======================================"
    read -p "Select an option: " choice
    
    case $choice in
        1)
            docker compose up -d postgres redis
            echo "Infrastructure started!"
            ;;
        2)
            docker compose up -d
            echo "All services started via Docker!"
            ;;
        3)
            echo "Starting local services..."
            
            [ -z "$GEMINI_API_KEY" ] && echo "Warning: GEMINI_API_KEY is not set! Features may not work."
            
            # Ensure tools are installed via mise
            echo "Installing and ensuring mise tools (python, node)..."
            mise install
            
            # Setup/activate python venv
            if [ ! -d ".venv" ]; then
                echo "Creating python environment..."
                mise exec -- python -m venv .venv
                source .venv/bin/activate
                pip install -r backend/requirements.txt
                pip install -r workers/requirements.txt
            else
                source .venv/bin/activate
            fi
            
            # Run Migrations
            echo "Running migrations..."
            export PYTHONPATH=.
            python scripts/migrate_db.py
            
            # Start Backend
            echo "Starting Backend API..."
            uvicorn backend.main:app --host localhost --port 8000 --reload &
            BACKEND_PID=$!
            
            # Start Workers
            echo "Starting Worker..."
            python -m workers.worker &
            WORKER_PID=$!
            
            # Start Frontend
            echo "Starting Frontend..."
            cd frontend
            mise exec -- npm install
            mise exec -- npm run dev &
            FRONTEND_PID=$!
            cd ..
            
            echo "Services started. Press [CTRL+C] to stop local services and return."
            
            trap cleanup SIGINT
            wait
            trap - SIGINT
            ;;
        4)
            echo "Stopping all services via Docker..."
            docker compose down
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option."
            ;;
    esac
done
