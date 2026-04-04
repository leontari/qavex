# New Service Template

Use this template when creating a new microservice.

---

## 📁 Folder Structure

```
services/<service-name>/
├── src/
│     └── main.py
├── tests/
├── requirements.txt
├── Dockerfile
├── Dockerfile.dev
├── README.md
└── pyproject.toml (optional)
```

---

## 🚀 Quick Start

### Create the folder

```bash
mkdir services/<service-name>
```

### Add boilerplate
```
cp -r services/api-gateway/* services/<service-name>
```

Or use the provided script:

```
make new-service name=<service-name>
```

---

## 🧩 main.py Example
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## 🐳 Dockerfile Example
```
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Tests

Place tests in:
```
services/<service-name>/tests/
```
Run:
```
pytest
```

---

## 🧱 Registering the Service
1. Add deployment templates in deploy/helm/app/templates/
2. Add service values in deploy/helm/app/values.yaml
3. Add routes to Traefik ingress if needed
4. Add service to docker-compose if used locally

---

## 🎉 Done!

Your new service is ready to run:
```
make run service=<service-name>
```
