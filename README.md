# Product Catalogue - DevOps Project

Django REST API demonstrating complete CI/CD automation with security scanning, containerization, and Kubernetes deployment.

[![CI/CD Pipeline](https://github.com/kech45/product-catalogue-devops/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/kech45/product-catalogue-devops/actions)

---

## Overview

Simple product catalog REST API built with Django and PostgreSQL (Supabase). Focus on DevOps automation, not application complexity.

**Features:**
- CRUD operations for products
- RESTful API with Django REST Framework
- PostgreSQL database via Supabase
- Complete CI/CD pipeline
- Security scanning (SAST)
- Kubernetes deployment

---

## CI/CD Pipeline

Following the project workflow exactly:

### Pipeline Steps

**1. Open Issue → Create Feature Branch → Unit Test → Linter → Style Check → SAST**
- Create issue for work tracking
- Create feature branch: `feature/your-feature`
- **Unit Tests** - pytest validates functionality
- **Linter** - Flake8 checks code quality
- **Style Check** - Black ensures formatting
- **SAST** - Bandit scans for security issues

**2. Build Docker Image → Scan for Vulnerabilities**
- Multi-stage Docker build
- Trivy scans image for CVEs

**3. Test SQL Deltas**
- Validate Django migrations
- Check for pending migrations

**4. Push to Central Repository → Rolling Deploy to Kubernetes**
- Push Docker image to Docker Hub
- Deploy to Kubernetes with zero downtime

**Pipeline Duration:** ~3 minutes

---

### What is SAST?

SAST analyzes source code and dependencies for security vulnerabilities **before** the application runs. It's like a security audit that happens automatically on every commit.

### Why SAST Matters

**The Problem:**
- Security bugs found in production are **10x more expensive** to fix
- Manual security reviews are slow and inconsistent
- Developers may not know security best practices

**The Solution:**
- Catch vulnerabilities during development
- Automated security checks on every commit
- Fast feedback loop (results in minutes)

### Tools Used

#### 1. Bandit - Python Security Scanner

Analyzes Python code for common security issues.

**What it detects:**
- **Hardcoded secrets** (passwords, API keys)
- **SQL injection** vulnerabilities
- **Insecure functions** (eval, exec, pickle)
- **Weak cryptography** (MD5, DES)
- **Command injection** risks
- **XSS vulnerabilities**


```

**Configuration (.bandit):**
```yaml
exclude_dirs:
  - /tests/
  - */migrations/*
skips:
  - B101  # Assert used (okay in tests)
```


**Running Bandit:**
```bash
# In pipeline
bandit -r catalogue/ -f json -o bandit-report.json

# Locally
bandit -r catalogue/
```

#### 2. Safety - Dependency Vulnerability Scanner

Checks Python packages against a database of known vulnerabilities.

**What it detects:**
- Known CVEs in dependencies
- Outdated packages with security patches
- Vulnerable package versions

 REPORT 

  -> django <4.2.11 affected by CVE-2024-27351
     Potential SQL injection in QuerySet.values() and values_list()
     
  -> psycopg2 <2.9.9 affected by CVE-2023-1234
     Buffer overflow in libpq connection handling
```

**Running Safety:**
```bash
# In pipeline
safety check --json

# Locally with output
safety check
```

#### 3. Trivy - Container Image Scanner

Scans Docker images for vulnerabilities in OS packages and application dependencies.

**What it scans:**
- OS packages (apt, apk, yum)
- Application dependencies (pip, npm, gem)
- Known CVEs from NVD database
- Misconfigurations

**Severity Levels:**
- **CRITICAL** - Immediate action required (pipeline fails)
- **HIGH** - Fix before deployment (pipeline fails)
- **MEDIUM** - Fix in next sprint
- **LOW** - Optional fix


**Running Trivy:**
```bash
# Scan image
trivy image product-catalogue:latest

# Fail on CRITICAL/HIGH only
trivy image --severity CRITICAL,HIGH --exit-code 1 product-catalogue:latest
```

### SAST Workflow in CI/CD

```
Developer pushes code -> Unit Tests -> Linter (Flake8) -> Style Check (Black) - > SAST Scanning (Bandit/Safety)- for scanning python code (Bandit), for scanning dependencies (Safety) -> if something critical found -> Pipeline FAILS and Developer is notified

```

### SAST Benefits

**Before SAST:**
- Security issues found in production
- Manual code reviews miss vulnerabilities
- Costly emergency patches
- Potential data breaches

**After SAST:**
- ✅ Vulnerabilities caught in development
- ✅ Automated on every commit
- ✅ Fast feedback (< 2 minutes)
- ✅ Prevents insecure code from reaching production
- ✅ Educates developers on security


## Project Structure

```
product-catalogue-devops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # Complete CI/CD pipeline
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── catalogue/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── .coverage
├── .dockerignore
├── .gitignore
├── .env
├── manage.py
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .flake8
├── .bandit.ini
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/{id}/` | Get product details |
| POST | `/api/products/` | Create product |
| PUT | `/api/products/{id}/` | Update product |
| DELETE | `/api/products/{id}/` | Delete product |

**Example:**
```bash
# Create product
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 1299.99,
    "stock": 50
  }'

# List products
curl http://localhost:8000/api/products/
```

---

## Setup & Running

### Prerequisites
- Python 3.12
- Docker & Docker Compose
- Kubernetes cluster (Minikube/K3s)
- Docker Hub account
- Supabase PostgreSQL database

---

## GitHub Actions Setup

Add these secrets in GitHub repository settings:

1. **DOCKER_USERNAME** - Your Docker Hub username
2. **DOCKER_PASSWORD** - Your Docker Hub password/token
3. **DATABASE_URL** - Supabase PostgreSQL connection string
4. **SECRET_KEY** - Django secret key

Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

---

## Technologies Used

| Category | Technology |
|----------|-----------|
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL (Supabase) |
| Language | Python 3.12 |
| CI/CD | GitHub Actions |
| Security | Bandit, Safety, Trivy |
| Quality | Flake8, Black, pytest |
| Container | Docker, Docker Compose |
| Orchestration | Kubernetes |
| Server | Gunicorn |

---

## DevOps Topics Demonstrated

✅ **Source Control** - Git with GitHub  
✅ **Branching Strategy** - Feature branches + Pull Requests  
✅ **Build Pipeline** - GitHub Actions (9 jobs)  
✅ **Continuous Integration** - Automated testing  
✅ **Continuous Delivery** - Docker build & push  
✅ **Security (SAST)** - Bandit, Safety, Trivy  
✅ **Code Quality** - Linting (Flake8) + Style (Black)  
✅ **Containerization** - Docker multi-stage builds  
✅ **Orchestration** - Kubernetes deployment  
✅ **Database Migrations** - Django migrations  
✅ **Infrastructure as Code** - Kubernetes manifests  

---

## Pipeline Summary

```
┌─────────────────────────────────────────────────────────┐
│                   CI/CD Pipeline Flow                   │
└─────────────────────────────────────────────────────────┘

1. Code Push/PR
   ↓
2. Unit Tests (pytest)         ← ~1 min
   ↓
3. Linter (Flake8)             ← ~30 sec
   ↓
4. Style Check (Black)         ← ~15 sec
   ↓
5. SAST (Bandit + Safety)      ← ~30 sec  
   ↓
6. Build Docker Image          ← ~1 min
   ↓
7. Scan Image (Trivy)          ← ~1 min
   ↓
8. Test Migrations             ← ~30 sec
   ↓
9. Push to Docker Hub          ← ~30 sec  (main branch only)


```

## Contributing

1. Create an issue
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature/your-feature`
5. Open Pull Request
6. Wait for CI/CD pipeline to pass
7. Merge to main

---