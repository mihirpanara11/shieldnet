.PHONY: install test test-unit test-integration lint dashboard-dev
.PHONY: docker-up docker-down docker-up-soc docker-down-soc
.PHONY: train train-lstm train-ae train-classifier train-if evaluate

# === Development ===

install:
	pip install -r requirements.txt

test: test-unit test-integration

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	python -m py_compile $$(find . -name '*.py' -not -path './*cache*')

# === Dashboard ===

dashboard-dev:
	cd dashboard && npm run dev

dashboard-build:
	cd dashboard && npm run build

# === Docker ===

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-up-soc:
	docker-compose -f docker-compose.soc.yml up -d

docker-down-soc:
	docker-compose -f docker-compose.soc.yml down

docker-rebuild:
	docker-compose build --no-cache

docker-logs:
	docker-compose logs -f

# === Training ===

train-lstm:
	python train/train_lstm.py --data data/cic-iot-2023.parquet

train-ae:
	python train/train_autoencoder.py --data data/cic-iot-2023.parquet

train-classifier:
	python train/train_classifier.py --data data/cic-iot-2023.parquet

train-if:
	python train/init_isolation_forest.py --data data/cic-iot-2023.parquet

train: train-lstm train-ae train-classifier train-if

evaluate:
	python train/evaluate_models.py

# === Attack Simulation ===

attack-ddos:
	python tests/attack_scenarios/inject_ddos.py --target-device TRF-0042

attack-botnet:
	python tests/attack_scenarios/inject_botnet.py --zone ZONE-04

attack-scan:
	python tests/attack_scenarios/inject_scan.py --target-device TRF-0042

# === gRPC ===

proto:
	python -m grpc_tools.protoc -I proto/ --python_out=. --grpc_python_out=. proto/*.proto
