build-docker-image:
	docker build --build-arg SSH_PRIVATE_KEY="$(shell cat ~/.ssh/id_rsa)" \
				 --build-arg SSH_PUBLIC_KEY="$(shell cat ~/.ssh/id_rsa.pub)" \
				 -t somlier-dev -f Dockerfile.dev .

prepare-e2e-environment:
	docker-compose -f docker-compose.dev.yml up -d

attach-e2e-environment: prepare-e2e-environment
	docker-compose -f docker-compose.dev.yml exec somlier bash

run-e2e-test: prepare-e2e-environment
	docker-compose -f docker-compose.dev.yml exec somlier bash -c "pytest tests/e2e -s"

run-integration-test:
	python3 -m pytest tests/integration

run-load-test-server:
	python3 -m locust -f tests/load/locustfile.py

run-unit-test:
	poetry run python3 -m pytest tests/unit

run-tests: prepare-e2e-environment
	@docker run --network socar-data-somlier_mlflow somlier-dev

run-rest-online-server:
	python3 -m somlier online server

run-compose-rest-online-server:
	docker-compose -f docker-compose.dev.yml exec somlier bash -c "python3 -m somlier online server"
