# Thought Aggregator

A powerful? platform designed to capture, analyze, and simulate thoughts and interactions using advanced AI. This project treats cognitive processes as structured data, enabling deep insights into sentiment, cognitive distortions, and behavioral patterns.

## Tools & Features

This project provides a suite of tools for thought analysis and generation:

### Thought Management & Analysis

- **Thought Collector**: A central repository to store and organize thoughts.
- **Cognitive Distortion Analyzer**: Automatically detects and categorizes cognitive distortions in thoughts (e.g., catastrophizing, black-and-white thinking).
- **Sentiment Analyzer**: Evaluates the emotional tone of each thought to track mood patterns.
- **Action Orientation Classifier**: Determines whether a thought is actionable or purely contemplative.
- **Thought Type Classifier**: Categorizes thoughts into different types for better organization.

### Persona Engine

- **Persona Creator**: Define digital personas with specific attributes (age, gender, personality traits).
- **Persona Derivation**: Create new personas based on existing ones or generate them entirely from a collection of thoughts.
- **Thought Generator**: scrape external content (e.g., blogs) and generate thoughts that mimic a specific persona's style and perspective.

### Creative & Interactive Tools

- **Essay Generator**: Collaborate with an AI persona to co-author essays, leveraging their unique perspective.
- **Conversation Simulator**: Orchestrate and simulate realistic conversations between multiple personas to explore different viewpoints and interactions.

## Setup & Installation

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.
- A [Google Gemini API Key](https://ai.google.dev/) for AI functionalities.

### Quick Start

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd thought-aggregator
    ```

2.  **Configure Environment Variables**
    Create a `.env` file in the root directory. You can use the template below.

3.  **Run with Docker Compose**
    ```bash
    docker-compose up --build
    ```
    This will start all services:
    - **Backend API**: Available at `http://localhost:8000`
    - **Frontend**: Available at `http://localhost:3002`
    - **Database (Postgres)**: Port `5432`
    - **Redis**: Port `6379`
    - **Background Workers**: For processing analysis and generation tasks.

## Environment Variables Template

Create a `.env` file in the root directory with the following content:

```env
# Database Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=thoughts
DATABASE_URL=postgresql://user:password@postgres:5432/thoughts

# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Worker Queue Configuration
# Comma-separated list of queues for workers to listen to
QUEUES=distortions,sentiment,generation,essay,action_orientation,thought_type,topics

# Frontend Configuration (if running locally outside docker)
VITE_API_URL=http://localhost:8000
```

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite (TypeScript, MUI)
- **Database**: PostgreSQL
- **Task Queue**: Redis + RQ (Redis Queue)
- **AI Engine**: Google Gemini
