# KI Self Sustain - Installationsanleitung

## 🚀 Schnellstart

### 1. Voraussetzungen prüfen

Stellen Sie sicher, dass folgende Software installiert ist:

```bash
# Docker prüfen
docker --version
# Sollte: Docker version 20.10.x oder höher

# Docker Compose prüfen
docker-compose --version
# Sollte: docker-compose version 1.29.x oder höher

# Verfügbarer Speicher (mindestens 20GB)
df -h
```

### 2. Projekt entpacken

```bash
# ZIP-Datei entpacken
unzip KI_Self_Sustain_Complete.zip
cd ki_self_sustain
```

### 3. Berechtigungen setzen

```bash
# Scripts ausführbar machen
chmod +x scripts/*.sh
```

### 4. System einrichten und starten

```bash
# Automatische Einrichtung
./scripts/setup.sh
```

Das Setup-Script führt folgende Schritte aus:
- Erstellt notwendige Verzeichnisse
- Setzt Berechtigungen
- Baut Docker-Images
- Startet alle Services
- Lädt LLM-Modell herunter
- Prüft Service-Status

### 5. System testen

Nach dem Setup sollten folgende URLs erreichbar sein:

- **Frontend**: http://localhost (Hauptanwendung)
- **Backend API**: http://localhost:5000/api/ai/status
- **Flowise**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

## 🔧 Manuelle Installation

Falls das automatische Setup fehlschlägt:

### 1. Verzeichnisse erstellen

```bash
mkdir -p data logs backups flowise_data llm_models redis_data
mkdir -p monitoring/prometheus_data monitoring/grafana_data
```

### 2. Docker Images bauen

```bash
# Backend bauen
docker-compose build backend

# Frontend bauen
docker-compose build frontend
```

### 3. Services starten

```bash
# Alle Services starten
docker-compose up -d

# Status prüfen
docker-compose ps
```

### 4. LLM-Modell installieren

```bash
# Warten bis Ollama gestartet ist
sleep 60

# Llama3 Modell herunterladen
docker-compose exec llm_service ollama pull llama3
```

## 🛠️ Konfiguration

### Umgebungsvariablen anpassen

Kopieren Sie `.env` zu `.env.local` und passen Sie die Werte an:

```bash
cp .env .env.local
nano .env.local
```

Wichtige Einstellungen:

```bash
# Flowise Zugangsdaten
FLOWISE_USERNAME=admin
FLOWISE_PASSWORD=ihr_sicheres_passwort

# LLM Konfiguration
LLM_MODEL=llama3  # oder ein anderes Modell

# Sicherheit
ENABLE_SAFETY_CHECKS=true
MAX_IMPROVEMENTS_PER_HOUR=5
```

### Ports anpassen

Falls Ports bereits belegt sind, ändern Sie diese in `docker-compose.yaml`:

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Statt Port 80
  
  backend:
    ports:
      - "5001:5000"  # Statt Port 5000
```

## 🔍 Troubleshooting

### Häufige Probleme

#### 1. Port bereits belegt

```bash
# Belegte Ports finden
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :5000

# Ports in docker-compose.yaml ändern
```

#### 2. Nicht genügend Speicher

```bash
# Speicher prüfen
free -h
df -h

# Docker aufräumen
docker system prune -a
```

#### 3. Services starten nicht

```bash
# Logs prüfen
docker-compose logs backend
docker-compose logs frontend
docker-compose logs flowise

# Service neu starten
docker-compose restart backend
```

#### 4. LLM-Modell lädt nicht

```bash
# Ollama Status prüfen
docker-compose exec llm_service ollama list

# Modell manuell laden
docker-compose exec llm_service ollama pull llama3
```

### Service-Status prüfen

```bash
# Alle Services
docker-compose ps

# Spezifische Service-Logs
docker-compose logs -f backend

# Service-Gesundheit
curl http://localhost:5000/api/ai/status
curl http://localhost:3000
```

### Neustart bei Problemen

```bash
# Kompletter Neustart
docker-compose down
docker-compose up -d

# Mit Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🔒 Sicherheit

### Erste Schritte nach Installation

1. **Passwörter ändern**
   ```bash
   # In .env.local
   FLOWISE_PASSWORD=ihr_neues_passwort
   GRAFANA_ADMIN_PASSWORD=ihr_neues_passwort
   ```

2. **Firewall konfigurieren**
   ```bash
   # Nur notwendige Ports öffnen
   sudo ufw allow 80
   sudo ufw allow 5000
   sudo ufw enable
   ```

3. **SSL/TLS einrichten** (für Produktion)
   - Reverse Proxy mit nginx
   - Let's Encrypt Zertifikate
   - HTTPS-Weiterleitung

## 📊 Monitoring einrichten

### Grafana Dashboards importieren

1. Grafana öffnen: http://localhost:3001
2. Login: admin / ki_self_sustain_2024
3. Dashboards importieren:
   - System Overview
   - AI Learning Metrics
   - Security Monitoring

### Prometheus Targets prüfen

1. Prometheus öffnen: http://localhost:9090
2. Status → Targets prüfen
3. Alle Targets sollten "UP" sein

## 🚀 Produktions-Deployment

### Für Produktionsumgebung

1. **Environment auf Production setzen**
   ```bash
   ENVIRONMENT=production
   FLASK_ENV=production
   ```

2. **Ressourcen-Limits setzen**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

3. **Backup-Strategie implementieren**
   ```bash
   # Automatische Backups
   crontab -e
   # 0 2 * * * /path/to/backup_script.sh
   ```

4. **Monitoring erweitern**
   - Externe Monitoring-Services
   - Alerting konfigurieren
   - Log-Aggregation

## 📞 Support

Bei Problemen:

1. **Logs sammeln**
   ```bash
   docker-compose logs > system_logs.txt
   ```

2. **System-Info sammeln**
   ```bash
   docker version > system_info.txt
   docker-compose version >> system_info.txt
   uname -a >> system_info.txt
   ```

3. **Issue erstellen** mit:
   - Fehlerbeschreibung
   - Schritte zur Reproduktion
   - System-Logs
   - Konfigurationsdateien

---

**Viel Erfolg mit KI Self Sustain!** 🤖✨

