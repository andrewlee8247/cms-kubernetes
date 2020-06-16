docker-api:
	cd ~/cms-kubernetes/app/api; \
	docker build --tag=healthcare-predictions-api:v.1.1 .
	docker tag healthcare-predictions-api:v.1.1 gcr.io/healthcare-predictions/healthcare-predictions-api:v.1.1
	docker push gcr.io/healthcare-predictions/healthcare-predictions-api:v.1.1

docker-frontend:
	cd ~/cms-kubernetes/app/frontend; \
	docker build --tag=healthcare-predictions-frontend:v.1.1 .
	docker tag healthcare-predictions-frontend:v.1.1 gcr.io/healthcare-predictions/healthcare-predictions-frontend:v.1.1
	docker push gcr.io/healthcare-predictions/healthcare-predictions-frontend:v.1.1

deploy-api:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f deployments/api-deployment.yaml

service-api:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f services/api-service.yaml

deploy-frontend:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f deployments/frontend-deployment.yaml

service-frontend:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f services/frontend-service.yaml

api-scaling:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f pods/api-hpa.yaml

ingress:
	cd ~/cms-kubernetes/app/k8s; \
	kubectl apply --namespace healthcare-app -f services/ingress.yaml