"""
Application configuration package.

This package contains all configuration-related modules and resources
used by the application across different deployment environments.

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations
- wheel/package installations

Package contents:
- static application configuration
- environment-driven runtime settings
- strongly-typed configuration enums
- logging configuration templates
- infrastructure integration settings

Subpackages:
    settings:
        Environment-driven runtime configuration modules.

    logging:
        Logging configuration templates and resources.

Modules:
    app:
        Static immutable application configuration.

    enums:
        Shared configuration enums and typed constants.

Configuration sources:
    Runtime settings are loaded from:
    - environment variables
    - .env files
    - Docker/Kubernetes runtime environments
    - CI/CD secret stores

Design principles:
    - strict typing
    - immutable configuration
    - environment isolation
    - deployment portability
    - production-safe defaults
    - infrastructure separation
"""
