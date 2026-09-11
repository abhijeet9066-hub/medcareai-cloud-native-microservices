.PHONY: test deploy verify delete

test:
	python -m pytest -q services/patient/tests services/appointment/tests services/gateway/tests

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/config.yaml
	kubectl apply -f k8s/redis.yaml
	kubectl apply -f k8s/services.yaml
	kubectl apply -f k8s/ingress.yaml
	kubectl apply -f k8s/resilience.yaml
	kubectl apply -f k8s/networkpolicy.yaml

verify:
	kubectl get all -n medcareai
	kubectl get ingress,hpa,pdb,networkpolicy -n medcareai

delete:
	kubectl delete namespace medcareai --ignore-not-found
