"""
Bootstrap is a sole composition root package.

It creates an KernelContext alongside a Fastapi instance.

Package returns an KernelContext and not just a FastApi instance.

Bootstrap phases:
1. config
2. logging
3. observability
4. infrastructure
5. app wiring
6. runtime hooks
7. routes

template_app/
├── bootstrap/
│   ├── app.py
│   ├── container.py
│   ├── lifecycle.py
│   ├── observability.py
│   ├── routing.py
│   ├── middleware.py
│   ├── exceptions.py
│   ├── infrastructure.py
│   └── testing.py


bootstrap/runtime orchestration
"""
