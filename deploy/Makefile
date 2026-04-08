# Build all images
build:
	for service in api-gateway market-data analytics alert-service worker-service scheduler frontend; do \
		docker build -t registry/qavex/$$service:$(TAG) -f deploy/docker/$$service.Dockerfile . ; \
	done

# Push all images
push:
	for service in api-gateway market-data analytics alert-service worker-service scheduler frontend; do \
		docker push registry/qavex/$$service:$(TAG) ; \
	done

# Deploy via Helm
deploy:
	helm upgrade --install qavex deploy/helm/qavex -f deploy/helm/qavex/values-$(ENV).yaml

# ArgoCD sync
sync:
	argocd app sync qavex-$(ENV)
