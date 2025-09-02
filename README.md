# 📊 Services Status Tracker

This repository contains two main components:

* **`api`**: Exposes data for Grafana dashboards via REST endpoints.
* **`kafka_consumer`**: Consumes messages from the Kafka topic `zabbix.metrics`, tracks service status changes, and calculates SLA metrics in real-time.

---

## 🚀 Getting Started

### 1. Clone the Repository & Set Up the Virtual Environment

```bash
git clone <your-git-repo-url>
cd <repo-folder-name>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Configure Environment Variables

Create a `.env` file at the project root:

`~/services_status_tracker/.env`

Add the following environment variables:

```env
MAX_ITEMS=5
MONGO_URI=<YOUR_MONGODB_CONNECTION_STRING>
KAFKA_BROKERS=<BROKER01:PORT,BROKER02:PORT,BROKER03:PORT>
VALKEY_MASTER=<CHANGE_THAT>
VALKEY_PASSWORD=<YOUR_VALKEY_PASSWORD>
```

---

## 🧪 Running the Services Locally

### Run the REST API

```bash
fastapi dev api/main.py
```

Test the endpoint:

```bash
curl http://localhost:8000/api/v1/mock-data/realtime-status-and-sla
```

---

### Run the Kafka Consumer

```bash
python -m kafka_consumer.zabbix.main
```

---

## 🛠 Deploying as Linux Services

### 📡 Deploying the REST API

#### 1. Create a systemd unit file

```bash
sudo nano /etc/systemd/system/grafana_restapi.service
```

#### 2. Paste the following configuration

```ini
[Unit]
Description=Rest API endpoints for Grafana
After=network.target

[Service]
Type=simple
User=u000218
WorkingDirectory=/home/hosting.local/u000218/services_status_tracker
EnvironmentFile=/home/hosting.local/u000218/services_status_tracker/.env
ExecStart=/home/hosting.local/u000218/services_status_tracker/venv/bin/fastapi run /home/hosting.local/u000218/services_status_tracker/api/main.py --host 172.17.33.21
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### 3. Reload and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable grafana_restapi.service
sudo systemctl start grafana_restapi.service
```

---

### 🧿 Deploying the Kafka Consumer

#### 1. Create a systemd unit file

```bash
sudo nano /etc/systemd/system/kafka_consumer.service
```

#### 2. Paste the following configuration

```ini
[Unit]
Description=Kafka real-time consumer from zabbix.items topic
After=network.target

[Service]
Type=simple
User=u000218
WorkingDirectory=/home/hosting.local/u000218/services_status_tracker
EnvironmentFile=/home/hosting.local/u000218/services_status_tracker/.env
ExecStart=/home/hosting.local/u000218/services_status_tracker/venv/bin/python -u -m kafka_consumer.zabbix.main
Restart=on-failure
RestartSec=5
StandardOutput=file:/var/log/kafka/kafka_consumer.log
StandardError=file:/var/log/kafka/kafka_consumer.log
AppendOutput=true

[Install]
WantedBy=multi-user.target
```

#### 3. Reload and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable kafka_consumer.service
sudo systemctl start kafka_consumer.service
```

---

## 🧪 Tests

The `tests` directory contains several utility scripts to help validate different parts of the system:

* **`e2e.py`**: End-to-end testing script that sends NDJSON data to Kafka using a Kafka connector tool.
* **`ping_mongo.py`**: Simple script to check MongoDB connectivity.
* **`producer.py`**: Similar to `e2e`, but sends messages directly to Kafka.
* **`status_tracker.py`**: Unit test to verify the logic of tracking service status changes.

Run these tests independently based on what part of the system you want to validate.

---

## 📂 Project Structure

```bash
.
├── api/                    # REST API source code
│   └── main.py
├── kafka_consumer/        # Kafka consumer logic
│   └── zabbix/
│       └── main.py
├── tests/                 # Testing utilities
│   ├── e2e.py
│   ├── ping_mongo.py
│   ├── producer.py
│   └── status_tracker.py
├── .env                   # Environment variables (not committed)
├── requirements.txt       # Python dependencies
├── README.md
└── ...
```

---

## ✅ Notes

* Ensure you have proper access to Kafka, MongoDB, and Valkey (Redis-compatible service).
* Log directories (`/var/log/kafka/`) should exist and be writable by the service user.
* If using SELinux or AppArmor, you may need to adjust permissions for systemd services.

--- 

## 🎥 Live Demo

Watch the demo below:
[Watch the video](https://drive.google.com/file/d/13A3iLx3SFSEshnfglBvKc78esOZwV0Kc/view?usp=sharing)
 
