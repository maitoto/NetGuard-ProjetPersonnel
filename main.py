"""
IDS (Intrusion Detection System) — Point d'entrée.
Ce script lance le dashboard Flask et la capture réseau en parallèle.
Affiche les statistiques globales toutes les 30 secondes.
"""

import argparse
import time
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="IDS Python - Détection d'intrusion réseau")
    parser.add_argument("--iface",        default=None,  help="Interface réseau (ex: eth0)")
    parser.add_argument("--port",         default=5000,  type=int, help="Port du dashboard Flask")
    parser.add_argument("--no-dashboard", action="store_true",     help="Désactive le dashboard web")
    return parser.parse_args()


def main():
    args = parse_args()

    print("""
╔══════════════════════════════════════════╗
║   IDS — Intrusion Detection System       ║
║   Détection : Port Scan | Flood | DoS    ║
╚══════════════════════════════════════════╝
    """)

    # Lance le dashboard Flask (thread daemon)
    if not args.no_dashboard:
        from dashboard import start_dashboard
        start_dashboard(port=args.port)
        time.sleep(0.5)  # Laisse Flask démarrer

    # Lance la capture réseau (thread daemon)
    from sniffer import start_sniffing
    start_sniffing(interface=args.iface)

    print("[IDS] Surveillance active. Ctrl+C pour arrêter.\n")

    # Boucle principale : affiche les stats toutes les 30s
    try:
        from alerts import get_stats
        while True:
            time.sleep(30)
            stats = get_stats()
            print(f"[STATS] Total alertes : {stats['total']} | Par type : {stats['by_type']}")
    except KeyboardInterrupt:
        print("\n[IDS] Arrêt propre.")
        sys.exit(0)


if __name__ == "__main__":
    main()