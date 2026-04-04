Install Traefik into cluster:

```bash
helm repo add traefik https://traefik.github.io/charts
```

```bash
helm repo update
```

```bash
helm install traefik traefik/traefik -n traefik --create-namespace
```
