# Payment Orchestration Layer

## Overview

A production-style Payment Orchestration Layer built with FastAPI and PostgreSQL.

The system routes transactions across multiple payment gateways, provides failover handling, idempotency protection, webhook processing, reconciliation capabilities, and transaction state management.

---

## Features

* Multi-Gateway Payment Processing
* Intelligent Gateway Routing
* Circuit Breaker Pattern
* Payment State Machine
* Idempotency Protection
* Webhook Processing
* Reconciliation Engine
* Gateway Health Monitoring
* Docker Support
* Automated Testing

---

## Technology Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Pytest

---

## Project Structure

```text
app/
tests/
Dockerfile
docker-compose.yml
requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Run Tests

```bash
pytest
```

---

## Docker

```bash
docker-compose up --build
```

---

## Core Components

### Payment State Machine

Manages transaction lifecycle and state transitions.

### Intelligent Gateway Router

Selects the best gateway based on routing rules and health metrics.

### Circuit Breaker

Protects the system from repeatedly calling unhealthy gateways.

### Webhook Engine

Processes asynchronous payment notifications.

### Reconciliation Engine

Detects inconsistencies between internal records and gateway data.

---

## Author

Goutham KS
