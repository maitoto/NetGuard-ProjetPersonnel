import time
from datetime import datetime


alerts = []

SEVERITY_COLORS = {
    "LOW":      "\033[93m",   # Jaune
    "MEDIUM":   "\033[91m",   # Rouge clair
    "HIGH":     "\033[31m",   # Rouge foncé
    "CRITICAL": "\033[1;31m", # Rouge gras
}
RESET = "\033[0m"

def add_alert(alert_type: str, src_ip: str, detail: str, severity: str = "MEDIUM"):
    """Enregistre une alerte et l'affiche dans la console."""
    alert = {
        "id":        len(alerts) + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "type":      alert_type,
        "src_ip":    src_ip,
        "detail":    detail,
        "severity":  severity,
    }
    alerts.append(alert)

    color = SEVERITY_COLORS.get(severity, "")
    print(
        f"{color}[ALERTE {severity}] {alert['timestamp']} | "
        f"{alert_type} | {src_ip} | {detail}{RESET}"
    )

def get_alerts():
    """Retourne toutes les alertes (pour le dashboard)."""
    return list(reversed(alerts))

def get_stats():
    """Retourne des statistiques globales."""
    total = len(alerts)
    by_severity = {}
    by_type = {}

    for a in alerts:
        by_severity[a["severity"]] = by_severity.get(a["severity"], 0) + 1
        by_type[a["type"]]         = by_type.get(a["type"], 0) + 1

    return {
        "total":       total,
        "by_severity": by_severity,
        "by_type":     by_type,
    }