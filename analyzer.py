"""
Comme son nom l'indique, analyzer.py est le moteur d'analyse de l'application.
Détection d'intrusion.
Analyse chaque paquet réseau et déclenche des alertes si nécessaire.
"""

from collections import defaultdict
import time
from alerts import add_alert

# ── Seuils de détection ───────────────────────────────────────────────────────
PORT_SCAN_THRESHOLD  = 20   # Nb de ports différents par IP en < WINDOW secondes
FLOOD_THRESHOLD      = 100  # Nb de paquets par IP en < WINDOW secondes
WINDOW               = 5    # Fenêtre temporelle (secondes)

# Payloads suspects (injection, exploitation courante)
SUSPICIOUS_PATTERNS = [
    b"SELECT", b"UNION", b"DROP TABLE",  # SQL injection
    b"/etc/passwd", b"../",              # Path traversal
    b"<script>", b"eval(",               # XSS / code injection
    b"cmd.exe", b"/bin/sh",              # Shell injection
]


connection_log: dict[str, list] = defaultdict(list)


packet_log: dict[str, list] = defaultdict(list)


def _clean_old_entries(log: dict, ip: str, now: float):
    """Supprime les entrées hors de la fenêtre temporelle."""
    log[ip] = [entry for entry in log[ip] if now - entry[0] <= WINDOW]


def analyze_packet(packet):
    """
    Analyse un paquet Scapy et déclenche les alertes appropriées.
    Appelé pour chaque paquet capturé.
    """
    from scapy.layers.inet import IP, TCP, UDP

    if not packet.haslayer(IP):
        return

    ip_layer  = packet[IP]
    src_ip    = ip_layer.src
    now       = time.time()


    packet_log[src_ip].append((now,))
    _clean_old_entries(packet_log, src_ip, now)  # type: ignore

    pkt_count = len(packet_log[src_ip])
    if pkt_count == FLOOD_THRESHOLD:
        add_alert(
            alert_type="FLOOD / DoS",
            src_ip=src_ip,
            detail=f"{pkt_count} paquets en {WINDOW}s",
            severity="HIGH",
        )

    dst_port = None
    if packet.haslayer(TCP):
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        dst_port = packet[UDP].dport

    if dst_port is not None:
        connection_log[src_ip].append((now, dst_port))
        _clean_old_entries(connection_log, src_ip, now) 

        unique_ports = {entry[1] for entry in connection_log[src_ip]}
        if len(unique_ports) >= PORT_SCAN_THRESHOLD:
            add_alert(
                alert_type="PORT SCAN",
                src_ip=src_ip,
                detail=f"{len(unique_ports)} ports scannés en {WINDOW}s",
                severity="CRITICAL",
            )

    raw_payload = bytes(packet.payload) if packet.payload else b""
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.lower() in raw_payload.lower():
            add_alert(
                alert_type="PAYLOAD SUSPECT",
                src_ip=src_ip,
                detail=f"Pattern détecté : {pattern.decode(errors='replace')}",
                severity="MEDIUM",
            )
            break  