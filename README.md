# ShieldNet
### Intelligent Cyber Attack Detection and Response System for Smart City IoT Infrastructure
### INTELLIFY 2025 | Problem ID: ALPHA401 | Track: SOFTWARE

**Detect. Contain. Recover. Autonomously.**

## Architecture

- **Tier 1 — IoT Device Layer**: MQTT/CoAP/Zigbee/LoRaWAN devices
- **Tier 2 — Edge Gateway Layer**: Feature extraction → AI ensemble inference → AIRO response
- **Tier 3 — SOC Layer**: Central monitoring, federated learning aggregation, dashboard

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start edge services
docker-compose up -d

# Start SOC services
docker-compose -f docker-compose.soc.yml up -d

# Run tests
pytest tests/unit/ -v
```

## Project Structure

```
shieldnet/
├── inference/         — AI Ensemble Engine (LSTM + IF + AE + Classifier)
├── features/          — Feature Extraction (47 features, 4 protocol extractors)
├── airo/              — Automated Incident Response Orchestrator (5 playbooks)
├── fl_client/         — Federated Learning Client (Flower + DP)
├── fl_server/         — Federated Learning Server (FedAvg)
├── agent_api/         — Edge REST API (FastAPI)
├── soc_api/           — Central SOC API (FastAPI + WebSocket)
├── train/             — Training scripts (LSTM, AE, XGBoost, IF)
├── dashboard/         — React SOC Dashboard
├── k8s/               — Kubernetes manifests
├── ansible/           — Ansible playbooks
├── proto/             — gRPC protocol definitions
├── config/            — Mosquitto, Kafka, Zeek, Prometheus configs
└── tests/             — Unit, integration, attack scenario tests
```

## Key Components

| Component | Description |
|---|---|
| Feature Extractor | 47 features per message, online Welford normalization |
| LSTM Runner | 60-step temporal sequence, 128+64 LSTM layers |
| Isolation Forest | Per-device statistical outlier detection (200 estimators) |
| Autoencoder | Conv1D reconstruction, anomaly from MSE |
| Threat Classifier | XGBoost multi-class (7 threat types) |
| AIRO Engine | State machine with 5 automated playbooks, <2s containment |
| FL System | Flower + FedAvg + Differential Privacy (ε=1.0, δ=1e-5) |

## System Requirements

- Python 3.11+
- Docker 24+ with docker-compose
- 4 GB RAM minimum (16 GB recommended)
- Raspberry Pi 4B (4 GB) per edge node
- Ubuntu 24.04 LTS (primary target)

## Edge-First Design

All detection happens locally on edge gateways. Raw device data never leaves its zone.
Anonymized feature vectors and model gradients are the only data transmitted upstream.

## Protocol Support

- MQTT (Mosquitto, TLS 1.3)
- CoAP (constrained devices)
- Zigbee (smart home sensors)
- LoRaWAN (long-range, low-power)

## API Endpoints

### Edge Agent API (port 8000)
| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Service health (protected) |
| `/devices/status` | GET | Device status list (protected) |
| `/threats/report` | POST | Submit threat event (protected) |
| `/airo/override` | POST | Manual incident response override (protected) |

### SOC API (port 8080)
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/incidents` | GET | List incidents |
| `/api/v1/zones` | GET | Zone status |
| `/api/v1/devices` | GET | Device profiles |
| `/api/v1/federated/status` | GET | FL status |
| `/ws/alerts` | WebSocket | Real-time alert stream |

## Training

```bash
# Train LSTM model
python train/train_lstm.py --data data/cic-iot-2023.parquet

# Train Autoencoder
python train/train_autoencoder.py --data data/cic-iot-2023.parquet

# Train XGBoost Threat Classifier
python train/train_classifier.py --data data/cic-iot-2023.parquet

# Initialize Isolation Forest per device
python train/init_isolation_forest.py --data data/cic-iot-2023.parquet

# Evaluate all models
python train/evaluate_models.py
```

## Verification

```bash
# Syntax check
python -c "
import py_compile, os
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            py_compile.compile(os.path.join(root, f), doraise=True)
print('All files pass')
"

# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Attack scenario injection
python tests/attack_scenarios/inject_ddos.py --target-device TRF-0042
```

## License

INTELLIFY 2025 — ALPHA401 — TRACK: SOFTWARE
