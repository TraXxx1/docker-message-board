# 🐳 Docker Message Board

A simple **containerized message board** application built to practice **Docker and container orchestration**.  
It demonstrates how multiple services (frontend, backend, database, cache, proxy) work together inside docker using Docker compose.

## Architecture
```
Browser → NGINX → Node.js Frontend + Flask API → PostgreSQL + Redis
```

**Services:**
- **NGINX**: Entry point - routes all web traffic to correct services
- **Frontend**: Node.js server serves the web page and user interface
- **API**: Flask REST API processes messages and handles business logic
- **Redis**: Caching layer for message counts
- **PostgreSQL**: Stores all messages permanently

## Quick Start

```bash
git clone https://github.com/TraXxx1/docker-message-board.git
cd docker-message-board
docker-compose up --build
```
**Note:** You gotta have docker components and dokcer-compose installed im your machine

**Visit:** http://localhost:8080

## Usage
1. Open http://localhost:8080 in your browser
2. Type a message and click "Post"
3. Messages are saved to PostgreSQL
4. Message counts cached in Redis at http://localhost:8080/api/count

