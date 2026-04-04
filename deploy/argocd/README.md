# ArgoCD: app-of-apps

ArgoCD installation (inside cluster):
```bash
kubectl create namespace argocd
```
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

After installation into cluster:
```bash
make argo-bootstrap
```

ArgoCD will deploy itself Helm chart from the repo.
