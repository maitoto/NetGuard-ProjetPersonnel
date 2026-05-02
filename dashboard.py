"""
Dashboard web Flask pour visualiser les alertes en temps réel.
Accessible sur http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template_string
from alerts import get_alerts, get_stats

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IDS Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Courier New', monospace; background: #0d1117; color: #c9d1d9; }

    header {
      background: #161b22;
      border-bottom: 1px solid #21262d;
      padding: 16px 32px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    header h1 { font-size: 18px; color: #58a6ff; letter-spacing: 2px; }
    .badge {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
      background: #1f6feb;
      color: #fff;
      font-weight: bold;
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 16px;
      padding: 24px 32px 0;
    }
    .stat-card {
      background: #161b22;
      border: 1px solid #21262d;
      border-radius: 8px;
      padding: 16px;
    }
    .stat-card .label { font-size: 12px; color: #8b949e; margin-bottom: 6px; }
    .stat-card .value { font-size: 28px; font-weight: bold; color: #58a6ff; }

    .alerts-section { padding: 24px 32px; }
    .alerts-section h2 { font-size: 14px; color: #8b949e; margin-bottom: 12px; letter-spacing: 1px; }

    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th {
      background: #161b22;
      color: #8b949e;
      text-align: left;
      padding: 10px 14px;
      font-size: 11px;
      letter-spacing: 1px;
      border-bottom: 1px solid #21262d;
    }
    td { padding: 10px 14px; border-bottom: 1px solid #161b22; }
    tr:hover td { background: #161b22; }

    .severity { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .severity-LOW      { background: #3d4f1f; color: #b5f09a; }
    .severity-MEDIUM   { background: #5c3a00; color: #f0a500; }
    .severity-HIGH     { background: #5c1a1a; color: #f07070; }
    .severity-CRITICAL { background: #3b0a0a; color: #ff4444; animation: blink 1s infinite; }

    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.5} }

    .refresh { float: right; font-size: 12px; color: #3fb950; cursor: pointer; text-decoration: underline; }
    .empty { color: #8b949e; text-align: center; padding: 32px; font-size: 14px; }
  </style>
</head>
<body>
  <header>
    <h1>&#9632; IDS MONITOR</h1>
    <span class="badge">LIVE</span>
  </header>

  <div class="stats" id="stats">
    <div class="stat-card">
      <div class="label">TOTAL ALERTES</div>
      <div class="value" id="total">0</div>
    </div>
    <div class="stat-card">
      <div class="label">CRITIQUES</div>
      <div class="value" style="color:#ff4444" id="critical">0</div>
    </div>
    <div class="stat-card">
      <div class="label">HIGH</div>
      <div class="value" style="color:#f07070" id="high">0</div>
    </div>
    <div class="stat-card">
      <div class="label">MEDIUM</div>
      <div class="value" style="color:#f0a500" id="medium">0</div>
    </div>
  </div>

  <div class="alerts-section">
    <h2>ALERTES DÉTECTÉES <span class="refresh" onclick="refresh()">↻ Actualiser</span></h2>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>HEURE</th>
          <th>TYPE</th>
          <th>IP SOURCE</th>
          <th>DÉTAIL</th>
          <th>SÉVÉRITÉ</th>
        </tr>
      </thead>
      <tbody id="alerts-body">
        <tr><td colspan="6" class="empty">Aucune alerte — surveillance en cours...</td></tr>
      </tbody>
    </table>
  </div>

  <script>
    async function refresh() {
      const [alertsRes, statsRes] = await Promise.all([
        fetch('/api/alerts'),
        fetch('/api/stats')
      ]);
      const alerts = await alertsRes.json();
      const stats  = await statsRes.json();

      // Stats
      document.getElementById('total').textContent    = stats.total;
      document.getElementById('critical').textContent = stats.by_severity?.CRITICAL || 0;
      document.getElementById('high').textContent     = stats.by_severity?.HIGH     || 0;
      document.getElementById('medium').textContent   = stats.by_severity?.MEDIUM   || 0;

      // Table
      const tbody = document.getElementById('alerts-body');
      if (alerts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty">Aucune alerte — surveillance en cours...</td></tr>';
        return;
      }
      tbody.innerHTML = alerts.map(a => `
        <tr>
          <td style="color:#8b949e">${a.id}</td>
          <td style="color:#8b949e">${a.timestamp}</td>
          <td style="color:#58a6ff">${a.type}</td>
          <td>${a.src_ip}</td>
          <td style="color:#c9d1d9">${a.detail}</td>
          <td><span class="severity severity-${a.severity}">${a.severity}</span></td>
        </tr>
      `).join('');
    }

    // Actualisation automatique toutes les 3 secondes
    refresh();
    setInterval(refresh, 3000);
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/api/alerts")
def api_alerts():
    return jsonify(get_alerts())

@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


def start_dashboard(host: str = "127.0.0.1", port: int = 5000):
    """Lance le serveur Flask dans un thread daemon."""
    import threading
    thread = threading.Thread(
        target=lambda: app.run(host=host, port=port, debug=False, use_reloader=False),
        daemon=True,
    )
    thread.start()
    print(f"[IDS] Dashboard disponible sur http://{host}:{port}")
    return thread