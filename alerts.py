"""
Que va servir "alterts.py" ? 
Il va permettre de gérer les alertes dans l'application.
Stocke les alertes en mémoire et les affiche dans la console.

"""

alerts = []

def add_alert(alert_type: str, src_ip: str, detail: str, severity: str = "MEDIUM"):
    from datetime import datetime

    alert = {
        "id":        len(alerts) + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "type":      alert_type,
        "src_ip":    src_ip,
        "detail":    detail,
        "severity":  severity,
    }
    alerts.append(alert)

def get_alerts():
    return list(reversed(alerts))


def get_stats():

    total = len(alerts)
    by_severity = {}
    by_type = {}

    for a in alerts:
        by_severity[a["severity"]] = by_severity.get(a["severity"], 0) + 1
        by_type[a["type"]] = by_type.get(a["type"], 0) + 1

    return {
        "total":       total,
        "by_severity": by_severity,
        "by_type":     by_type,
    }


"""
if __name__ == "__main__":
    add_alert("PORT SCAN",  "192.168.1.10", "22 ports scannés en 5s", "CRITICAL")
    add_alert("FLOOD",      "10.0.0.5",     "150 paquets en 5s",      "HIGH")
    add_alert("PAYLOAD",    "172.16.0.3",   "Pattern: /etc/passwd",   "MEDIUM")

    print("\n--- Stats ---")
    print(get_stats())

    print("\n--- Alertes ---")
    for a in get_alerts():
        print(a)
"""