.PHONY: up down logs build restart kind-up kind-down helm-deploy helm-delete argo-bootstrap

up:
	cd docker && docker-compose up -d

down:
	cd docker && docker-compose down

logs:
	cd docker && docker-compose logs -f

build:
	cd docker && docker-compose build

restart:
	cd docker && docker-compose down && docker-compose up -d

kind-up:
	kind create cluster --name dev --config ../deploy/kind/kind-config.yaml

kind-down:
	kind delete cluster --name dev

helm-deploy:
	helm upgrade --install app ../deploy/helm/app -n app --create-namespace

helm-delete:
	helm uninstall app -n app

argo-bootstrap:
	kubectl apply -n argocd -f ../deploy/argocd/app-of-apps.yaml
