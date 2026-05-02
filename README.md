# 🛡️ NetGuard — Intrusion Detection System
Intrusion Detection System en Python - Scapy + Flask*
> Système de détection d'intrusion réseau en Python — Projet personnel d'alternance en cybersécurité
---

## 📌 Présentation

**NetGuard** est un système de détection d'intrusion (IDS) développé en Python dans le cadre d'un projet personnel orienté cybersécurité. Il capture le trafic réseau en temps réel, analyse chaque paquet et déclenche des alertes en cas de comportement anormal.

Le projet s'inspire des problématiques rencontrées dans les environnements industriels et militaires (systèmes embarqués, réseaux critiques) et démontre des compétences en :

- **Capture réseau bas niveau** avec Scapy
- **Détection comportementale** par fenêtre temporelle glissante
- **Architecture modulaire** orientée séparation des responsabilités
- **API REST** et dashboard web en temps réel avec Flask
- **Programmation concurrente** (threading Python)

---

## 🎯 Fonctionnalités

| Détection | Description | Sévérité |
|-----------|-------------|----------|
| **Port Scan** | Détecte une IP qui sonde > 20 ports différents en 5s | CRITICAL |
| **Flood / DoS** | Détecte > 100 paquets/IP en 5s | HIGH |
| **Payload suspect** | Détecte des patterns d'injection dans les données (SQL, shell, XSS) | MEDIUM |

- ✅ Dashboard web en temps réel (auto-refresh toutes les 3s)
- ✅ API REST `/api/alerts` et `/api/stats`
- ✅ Alertes colorées dans la console (codes ANSI)
- ✅ Filtre BPF pour n'analyser que le trafic IP
- ✅ Architecture multi-thread (sniffer + dashboard indépendants)

---

## 🏗️ Architecture

```
NetGuard/
├── main.py          # Point d'entrée — orchestre tous les modules
├── sniffer.py       # Capture réseau Scapy (thread daemon)
├── analyzer.py      # Moteur de détection (flood, port scan, payload)
├── alerts.py        # Stockage et affichage des alertes
├── dashboard.py     # Serveur Flask + interface web
└── requirements.txt # Dépendances Python
```

**Flux de données :**
```
Trafic réseau
      ↓
  sniffer.py  ──── capture chaque paquet IP
      ↓
 analyzer.py  ──── analyse : flood ? scan ? payload suspect ?
      ↓
  alerts.py   ──── stocke + affiche en console
      ↓
 dashboard.py ──── expose via API REST → navigateur
```

---

## ⚙️ Installation

### Prérequis

- Python 3.10+
- Windows : installer **[Npcap](https://npcap.com/#download)** (driver réseau pour Scapy), en cochant *"WinPcap API-compatible mode"*
- Linux/Mac : `sudo` requis pour la capture réseau

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/maitoto/NetGuard-ProjetPersonnel.git
cd NetGuard-ProjetPersonnel

# 2. Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate.bat     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## 🚀 Utilisation

```bash
# Lancement standard (toutes les interfaces)
sudo python main.py

```

Le dashboard est accessible sur **http://127.0.0.1:5000**

---

## 🧪 Tests

Pour générer des alertes de test, ouvrir un second terminal :

```bash
# Simuler un flood UDP (déclenche alerte HIGH)
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(150):
    s.sendto(b'test', ('192.168.1.X', 9999))  # Remplacer par votre IP locale
print('Flood envoyé.')
"

# Simuler un payload SQL injection (déclenche alerte MEDIUM)
python -c "
import socket
s = socket.socket()
s.connect(('127.0.0.1', 80))
s.send(b'GET /?id=1 UNION SELECT * FROM users HTTP/1.0\r\n\r\n')
s.close()
"
```

> **Note :** Sur Windows, Scapy capte mal le trafic loopback (127.0.0.1). Utiliser votre adresse IP locale (`ipconfig` pour la trouver).

---

## 📡 API REST

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web du dashboard |
| `/api/alerts` | GET | Liste des alertes (JSON, antichronologique) |
| `/api/stats` | GET | Statistiques globales (JSON) |

**Exemple de réponse `/api/alerts` :**
```json
[
  {
    "id": 3,
    "timestamp": "14:32:05",
    "type": "PORT SCAN",
    "src_ip": "192.168.1.42",
    "detail": "25 ports différents scannés en 5s",
    "severity": "CRITICAL"
  }
]
```

---

## 🔧 Configuration

Les seuils de détection sont modifiables dans `analyzer.py` :

```python
PORT_SCAN_THRESHOLD = 20   # Ports uniques par IP dans la fenêtre
FLOOD_THRESHOLD     = 100  # Paquets par IP dans la fenêtre
WINDOW              = 5    # Fenêtre temporelle (secondes)
```

---

## 📈 Évolutions possibles

- [ ] Persistance des alertes en base de données (SQLite)
- [ ] Export des logs en CSV/JSON
- [ ] Détection d'ARP Spoofing
- [ ] Intégration SIEM (envoi d'alertes via syslog)
- [ ] Interface de configuration des seuils en temps réel
- [ ] Support IPv6

---

## 📄 Licence

Ce projet est sous licence MIT — libre d'utilisation à des fins éducatives et personnelles.
