#!/usr/bin/env python3
"""
LOCAD Dashboard Refresh Server
Listens on http://localhost:8765
  GET /refresh  → re-queries Metabase T69, regenerates HTML, pushes to GitHub Pages
  GET /status   → shows last refresh time

Usage: python3 refresh_server.py   (or double-click refresh_server.command)
"""

import getpass, glob, http.server, io, json, os, re, subprocess, sys, threading, zipfile
import urllib.request, urllib.error
from datetime import datetime, date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
PORT        = 8765
MB_URL      = "https://metabase.golocad.com"
MB_DB       = 2
T69         = 69
F_DATE      = 1710   # started_at_local
F_EMP_BY    = 1712   # employed_by
F_WAREHOUSE = 1708   # attendance_warehouse
WAREHOUSE   = "LOCAD Cabuyao (LISP) FC"
EMPLOYERS   = ["GREEN ARROW", "REVMAN", "TOPLIS Solutions"]
TODAY       = date.today().isoformat()          # e.g. "2026-06-17"
TODAY_LABEL = datetime.today().strftime("%-d %b")

CONFIG_PATH  = Path.home() / ".locad_dashboard.json"
SCRIPT_DIR   = Path(__file__).parent
GENERATE_PY  = SCRIPT_DIR / "generate_dashboard.py"
DEPLOY_PY    = SCRIPT_DIR / "netlify_deploy.py"
# GitHub Pages repo — HTML is published as index.html here
GITHUB_REPO  = Path.home() / "Desktop" / "locad-finops-dashboard"

last_refresh = "Never"
last_hc      = None

# ── Metabase helpers ──────────────────────────────────────────────────────────
def mb_session(user: str, pw: str) -> str:
    data = json.dumps({"username": user, "password": pw}).encode()
    req  = urllib.request.Request(
        f"{MB_URL}/api/session", data=data,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["id"]

def query_today_hc(token: str, day: str) -> int:
    """Return headcount for LOCAD Cabuyao filtered by employer list, for one day."""
    payload = {
        "database": MB_DB,
        "type": "query",
        "query": {
            "source-table": T69,
            "filter": ["and",
                ["=",  ["field", F_WAREHOUSE, {"base-type": "type/Text"}], WAREHOUSE],
                ["in", ["field", F_EMP_BY,    {"base-type": "type/Text"}]] + EMPLOYERS,
                ["between",
                    ["field", F_DATE, {"base-type": "type/DateTimeWithLocalTZ"}],
                    f"{day}T00:00:00", f"{day}T23:59:59"
                ]
            ]
        }
    }
    data = json.dumps({"query": payload}).encode()
    req  = urllib.request.Request(
        f"{MB_URL}/api/dataset", data=data,
        headers={"Content-Type": "application/json",
                 "X-Metabase-Session": token},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        result = json.loads(r.read())
    rows = result.get("data", {}).get("rows", [])
    return len(rows)

# ── Dashboard regeneration ────────────────────────────────────────────────────
def update_headcount_in_script(hc: int, day: str):
    """Patch the headcount for `day` inside generate_dashboard.py."""
    src = GENERATE_PY.read_text()
    pattern = rf"('{re.escape(day)}':\s*)\d+"
    new_src  = re.sub(pattern, rf"\g<1>{hc}", src)
    if new_src == src:
        print(f"  [warn] No pattern found for {day} — headcount not updated in script")
    else:
        GENERATE_PY.write_text(new_src)
        print(f"  Patched {day} headcount → {hc}")

def regenerate():
    result = subprocess.run(
        [sys.executable, str(GENERATE_PY)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"generate_dashboard.py failed:\n{result.stderr}")
    print("  HTML regenerated")

def deploy():
    """Copy regenerated HTML to GitHub Pages repo and push."""
    import shutil
    # Find the generated HTML (outputs next to generate_dashboard.py)
    src_html = SCRIPT_DIR / "locad-dashboard-latest.html"
    dst_html = GITHUB_REPO / "index.html"

    if not src_html.exists():
        raise RuntimeError(f"Generated HTML not found at {src_html}")
    if not GITHUB_REPO.exists():
        raise RuntimeError(f"GitHub repo folder not found at {GITHUB_REPO}")

    shutil.copy2(src_html, dst_html)
    print(f"  Copied HTML → {dst_html}")

    # Git commit and push
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    cmds = [
        ["git", "-C", str(GITHUB_REPO), "add", "index.html"],
        ["git", "-C", str(GITHUB_REPO), "commit", "-m", f"Refresh: headcount update {ts}"],
        ["git", "-C", str(GITHUB_REPO), "push"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
            raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{r.stderr}")
    print("  Pushed to GitHub Pages")

# ── Load / prompt for credentials ────────────────────────────────────────────
def ensure_credentials() -> dict:
    cfg = {}
    if CONFIG_PATH.exists():
        cfg = json.loads(CONFIG_PATH.read_text())

    if not cfg.get("mb_user") or not cfg.get("mb_pass"):
        print("\n── Metabase credentials needed for headcount refresh ──")
        cfg["mb_user"] = input("  Metabase email: ").strip()
        cfg["mb_pass"] = getpass.getpass("  Metabase password: ")
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
        print(f"  Saved to {CONFIG_PATH}\n")

    return cfg

# ── HTTP handler ──────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # suppress default access log
        pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        global last_refresh, last_hc

        if self.path in ("/refresh", "/refresh/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self._cors()
            self.end_headers()
            try:
                cfg   = ensure_credentials()
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Refresh triggered by browser")

                print("  Authenticating with Metabase…")
                token = mb_session(cfg["mb_user"], cfg["mb_pass"])

                print(f"  Querying T69 headcount for {TODAY}…")
                hc = query_today_hc(token, TODAY)
                print(f"  Headcount today: {hc}")

                update_headcount_in_script(hc, TODAY)
                regenerate()
                deploy()

                last_refresh = datetime.now().strftime("%H:%M:%S")
                last_hc      = hc
                msg = f"OK | {TODAY} HC updated to {hc} | refreshed at {last_refresh}"
                self.wfile.write(msg.encode())
                print(f"  Done ✓ ({msg})\n")
            except Exception as e:
                err = f"ERROR: {e}"
                self.wfile.write(err.encode())
                print(f"  {err}\n")

        elif self.path in ("/status", "/status/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({
                "last_refresh": last_refresh,
                "last_hc": last_hc,
                "today": TODAY,
            }).encode())

        else:
            self.send_response(404)
            self.end_headers()

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Quick credential check on startup (optional — won't block if skipped)
    print(f"\nLOCAD Dashboard Refresh Server")
    print(f"Listening on http://localhost:{PORT}")
    print(f"  /refresh  → fetch latest HC, regenerate, push to GitHub Pages")
    print(f"  /status   → last refresh info")
    print(f"\nKeep this window open. Click ↻ Refresh in the dashboard.\n")

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
