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

### Local Dataset Requirements

If you are running the application using Docker, the required Cornell Movie-Dialogs Corpus dataset is automatically downloaded into the `/app/data/cornell_dialogs` directory within the containers during the build process.

If you are running the application natively without Docker, you must manually download the dataset:

1. Download the dataset from: `http://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip`
2. Extract the `.zip` file.
3. Move the extracted files (e.g., `movie_lines.txt`, `movie_conversations.txt`) into `/app/data/cornell_dialogs` or the corresponding path expected by the backend service.

### Quick Start

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd thought-aggregator
    ```

2.  **Configure Environment Variables**
    Create a `.env` file in the root directory. You can use the template below.

3.  **Run Services**
    You can use the provided bash script to start the services either via Docker or locally on your machine.

    ```bash
    ./run.sh
    ```

    This will present a terminal menu with the following options:
    - **1. Start Infrastructure (Postgres/Redis) via Docker**: Useful if you want to run the core app code locally but need the databases active.
    - **2. Start All Services via Docker**: Runs everything, including the app and workers, isolated in Docker.
    - **3. Start Services Locally**: Starts the Backend, Workers, and Frontend natively on your machine (requires Postgres/Redis to be running via option 1 or manually). This will also set up a Python virtual environment automatically using `mise`.
    - **4. Stop All Docker Services**: Brings down the Docker Compose environment.
    - **5. Exit**

    If you choose to run everything via Docker (Option 2), the following services will be available:
    - **Backend API**: `http://localhost:8000`
    - **Frontend**: `http://localhost:3002`

    If you choose to run local services (Option 3), they will also use the same ports respectively.

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
