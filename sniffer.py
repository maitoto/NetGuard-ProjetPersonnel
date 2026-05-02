"""
Capture des paquets réseau avec Scapy.
Lance le sniffing dans un thread séparé.
"""

import threading
from scapy.all import sniff
from analyzer import analyze_packet


def _packet_callback(packet):
    """Callback appelé par Scapy pour chaque paquet capturé."""
    try:
        analyze_packet(packet)
    except Exception as e:
        print(f"[ERREUR] Analyse paquet : {e}")


def start_sniffing(interface: str = None, packet_count: int = 0):
    kwargs = {
        "prn":   _packet_callback,
        "store": False,   
        "count": packet_count,
        "filter": "ip",   
    }
    if interface:
        kwargs["iface"] = interface

    thread = threading.Thread(
        target=sniff,
        kwargs=kwargs,
        daemon=True,  
    )
    thread.start()
    print(f"[IDS] Sniffing démarré sur {'toutes interfaces' if not interface else interface}")
    return thread