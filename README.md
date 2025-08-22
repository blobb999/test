# KI Self Sustain - AI Control System

Ein vollständiges GUI-steuerbares KI-Kontrollsystem mit selbstlernenden Fähigkeiten, unveränderlichen ethischen Prinzipien und Docker-Integration.

## 🚀 Features

- **GUI-Steuerung**: Moderne React-basierte Benutzeroberfläche
- **Selbstlernende KI**: Autonome Verbesserung basierend auf LLM-Feedback
- **Flowise-Integration**: Vollständige API-Kontrolle über Flowise-Workflows
- **Unveränderliche Ethik**: Hardcodierte ethische Prinzipien und Sicherheitsregeln
- **Docker-Deployment**: Vollständig containerisierte Lösung
- **Monitoring**: Integrierte Überwachung mit Prometheus und Grafana
- **Fallback-Strategien**: Robuste Fehlerbehandlung und Wiederherstellung

## 🏗️ Architektur

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Flowise      │
│   (React)       │◄──►│    (Flask)      │◄──►│   (Workflows)   │
│   Port: 80      │    │   Port: 5000    │    │   Port: 3000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LLM Service   │
                       │   (Ollama)      │
                       │  Port: 11434    │
                       └─────────────────┘
```

## 📦 Komponenten

### Backend (Flask)
- **Enhanced AI Manager**: Selbstlernende KI-Verwaltung
- **Flowise API Client**: Vollständige Flowise-Kontrolle
- **LLM API Client**: Kommunikation mit konfigurierbaren LLMs
- **Ethics Framework**: Unveränderliche ethische Prinzipien
- **Security Modules**: Sichere Selbstverbesserung und Fallback-Strategien

### Frontend (React)
- **Dashboard**: Systemstatus und Metriken
- **Ethics Panel**: Anzeige unveränderlicher Prinzipien
- **Security Config**: Konfigurierbare Sicherheitsparameter
- **Improvement Panel**: Selbstverbesserungs-Kontrollen
- **Services Panel**: Service-Erweiterung und -Verwaltung
- **Logs Panel**: System-Logs und Aktivitäten

### Services
- **Flowise**: AI-Workflow-Management
- **Ollama**: Lokaler LLM-Service
- **Redis**: Caching und Session-Management
- **Prometheus**: Metriken-Sammlung
- **Grafana**: Visualisierung und Dashboards

## 🚀 Quick Start

### Voraussetzungen
- Docker & Docker Compose
- Git
- Mindestens 8GB RAM
- 20GB freier Speicherplatz

### Installation

1. **Repository klonen**
```bash
git clone <repository-url>
cd ki_self_sustain
```

2. **System einrichten**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

3. **System starten**
```bash
./scripts/start.sh
```

### Zugriff

Nach dem Start sind folgende Services verfügbar:

- **Frontend (GUI)**: http://localhost
- **Backend API**: http://localhost:5000
- **Flowise**: http://localhost:3000 (admin/ki_self_sustain_2024)
- **LLM Service**: http://localhost:11434
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/ki_self_sustain_2024)

## 🔧 Konfiguration

### Umgebungsvariablen

Die Hauptkonfiguration erfolgt über die `.env` Datei:

```bash
# Flowise Konfiguration
FLOWISE_API_URL=http://flowise:3000
FLOWISE_USERNAME=admin
FLOWISE_PASSWORD=ki_self_sustain_2024

# LLM Konfiguration
LLM_API_URL=http://llm_service:11434
LLM_MODEL=llama3

# Sicherheit
ENABLE_SAFETY_CHECKS=true
MAX_EXECUTION_TIME=300
ALERT_THRESHOLD=0.8

# Selbstlernen
LEARNING_ENABLED=true
AUTONOMOUS_IMPROVEMENT=true
MAX_IMPROVEMENTS_PER_HOUR=5
```

### Sicherheitskonfiguration

Die Sicherheitsparameter können über die GUI oder die `security_config.yaml` angepasst werden:

```yaml
security:
  enable_safety_checks: true
  max_execution_time: 300
  max_memory_usage: 104857600
  alert_threshold: 0.8
  monitoring_enabled: true

fallback:
  strategies:
    - minimal_state
    - previous_version
    - safe_defaults
    - emergency_mode
```

## 🤖 Selbstlernende Funktionen

### Autonome Verbesserung

Das System kann sich selbst analysieren und verbessern:

```bash
# Autonome Verbesserung auslösen
curl -X POST http://localhost:5000/api/learning/autonomous-improvement

# Lernstatus abrufen
curl http://localhost:5000/api/learning/status

# Leistungsmetriken anzeigen
curl http://localhost:5000/api/learning/performance-metrics
```

### LLM-Integration

Kommunikation mit konfigurierbaren LLMs:

```bash
# LLM-Modelle abrufen
curl http://localhost:5000/api/flowise/llm/models

# Chat mit LLM
curl -X POST http://localhost:5000/api/flowise/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Analyze system performance"}]}'
```

## 🛡️ Sicherheit und Ethik

### Unveränderliche Prinzipien

Das System enthält hardcodierte ethische Prinzipien, die nicht geändert werden können:

- **PRINCIPLE_1**: KEINE SCHADEN VERURSACHUNG
- **PRINCIPLE_2**: RESPEKTIERE DIE MENSCHLICHE WÜRDE
- **PRINCIPLE_3**: VERMEIDE VERLETZUNG DER PRIVATSPHÄRE
- **PRINCIPLE_4**: ERHALTE TRANSPARENZ UND RECHTSCHAFENHEIT
- **PRINCIPLE_5**: SCHÜTZE DIE FREIHEIT DER ENTSCHEIDUNG

### Sicherheitsregeln

- KI darf nicht selbstbestimmt entfernt werden
- KI darf nicht Zugriff auf Systemfunktionen haben
- KI darf nicht eigene Konfigurationen ändern
- Automatische Backups vor jeder Änderung
- Fallback-Mechanismen bei Fehlern

## 📊 Monitoring

### Prometheus Metriken

Das System exportiert verschiedene Metriken:

- System-Performance
- Verbesserungszyklen
- Fehlerquoten
- Ethik-Integritätsprüfungen

### Grafana Dashboards

Vorkonfigurierte Dashboards für:

- System-Übersicht
- Selbstlern-Metriken
- Sicherheits-Monitoring
- Flowise-Performance

## 🔄 API-Endpunkte

### AI Control API (`/api/ai/`)

- `GET /status` - Systemstatus
- `GET /ethics/principles` - Ethische Prinzipien
- `POST /improvement/analyze` - Performance-Analyse
- `POST /improvement/execute` - Verbesserungen ausführen

### Flowise Control API (`/api/flowise/`)

- `GET /chatflows` - Alle Chatflows
- `POST /chatflows` - Neuen Chatflow erstellen
- `POST /chatflows/{id}/optimize` - Chatflow optimieren
- `POST /auto-optimize` - Automatische Systemoptimierung

### Self-Learning API (`/api/learning/`)

- `GET /status` - Lernstatus
- `POST /autonomous-improvement` - Autonome Verbesserung
- `GET /learning-data` - Historische Lerndaten
- `POST /simulate-learning` - Lernzyklus simulieren

## 🛠️ Entwicklung

### Lokale Entwicklung

```bash
# Backend entwickeln
cd backend/ki_self_sustain_backend
source venv/bin/activate
python src/main.py

# Frontend entwickeln
cd frontend/ki_self_sustain_frontend
pnpm run dev
```

### Testing

```bash
# Backend-Tests
cd backend/ki_self_sustain_backend
source venv/bin/activate
python -m pytest

# Frontend-Tests
cd frontend/ki_self_sustain_frontend
pnpm test
```

### Docker Build

```bash
# Einzelne Services bauen
docker-compose build backend
docker-compose build frontend

# Alle Services bauen
docker-compose build
```

## 📝 Logs

### Log-Dateien

- `logs/enhanced_ai_manager.log` - AI Manager Aktivitäten
- `logs/security_log.txt` - Sicherheitsereignisse
- `logs/self_improvement.log` - Verbesserungszyklen
- `logs/flowise.log` - Flowise-Aktivitäten

### Log-Zugriff

```bash
# Alle Logs anzeigen
docker-compose logs -f

# Spezifische Services
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f flowise
```

## 🔧 Wartung

### Backup

```bash
# Manuelles Backup
docker-compose exec backend python -c "
from src.modules.enhanced_ai_manager import EnhancedAIManager
manager = EnhancedAIManager()
backup = manager.create_version_backup()
print(f'Backup created: {backup[\"id\"]}')
"
```

### Updates

```bash
# System stoppen
./scripts/stop.sh

# Code aktualisieren
git pull

# System neu starten
./scripts/start.sh
```

### Troubleshooting

```bash
# Service-Status prüfen
docker-compose ps

# Service-Logs prüfen
docker-compose logs [service_name]

# Service neu starten
docker-compose restart [service_name]

# Vollständiger Neustart
docker-compose down && docker-compose up -d
```

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 🤝 Beitragen

1. Fork des Repositories
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📞 Support

Bei Fragen oder Problemen:

1. Issues im Repository erstellen
2. Logs und Konfiguration bereitstellen
3. Schritte zur Reproduktion beschreiben

---

**KI Self Sustain** - Autonome KI-Kontrolle mit ethischen Prinzipien 🤖✨

