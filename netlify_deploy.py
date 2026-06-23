#!/usr/bin/env python3
"""Deploy locad-dashboard-latest.html to Netlify."""

import glob, io, json, logging, os, sys, zipfile
from pathlib import Path
from datetime import datetime
import urllib.request, urllib.error

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%H:%M")
log = logging.getLogger(__name__)

CONFIG_PATH = Path.home() / ".locad_dashboard.json"
FIXED_NAME  = "locad-dashboard-latest.html"
SEARCH_PATTERN = str(
    Path.home() / "Library" / "Application Support" / "Claude" /
    "local-agent-mode-sessions" / "**" / "outputs" / FIXED_NAME
)
FALLBACK = Path.home() / "Documents" / "locad-dashboard" / FIXED_NAME


def find_html():
    matches = glob.glob(SEARCH_PATTERN, recursive=True)
    if matches:
        return Path(max(matches, key=os.path.getmtime))
    if FALLBACK.exists():
        return FALLBACK
    return None


def load_config():
    if not CONFIG_PATH.exists():
        log.error(f"Config not found: {CONFIG_PATH}. Run netlify_setup.py first.")
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())


def make_zip(html_path: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", html_path.read_text(encoding="utf-8"))
        # Force Netlify to serve index.html as text/html
        zf.writestr("_headers", "/index.html\n  Content-Type: text/html; charset=utf-8\n")
    return buf.getvalue()


def deploy(site_id: str, token: str, zip_bytes: bytes) -> str:
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    req = urllib.request.Request(
        url,
        data=zip_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/zip",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data.get("deploy_ssl_url") or data.get("url", "unknown")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        log.error(f"Netlify API error {e.code}: {body}")
        sys.exit(1)


def main():
    cfg = load_config()
    html_path = find_html()
    if not html_path:
        log.warning(f"No dashboard HTML found. Checked:\n  {SEARCH_PATTERN}\n  {FALLBACK}")
        sys.exit(0)

    log.info(f"Deploying: {html_path}")
    zip_bytes = make_zip(html_path)
    url = deploy(cfg["site_id"], cfg["token"], zip_bytes)
    log.info(f"Deployed to {url} [done]")


if __name__ == "__main__":
    main()
