#!/bin/bash
# Double-click this file to regenerate and publish the dashboard to GitHub Pages.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$HOME/Desktop/locad-finops-dashboard"

echo "======================================"
echo " LOCAD FC FinOps Dashboard — Update"
echo "======================================"
echo ""

# Step 1: Regenerate HTML
echo "Step 1: Regenerating dashboard..."
python3 "$SCRIPT_DIR/generate_dashboard.py"
if [ $? -ne 0 ]; then
  echo "ERROR: Dashboard generation failed."
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi
echo "Done."
echo ""

# Step 2: Copy to GitHub repo
echo "Step 2: Copying to GitHub repo..."
cp "$SCRIPT_DIR/locad-dashboard-latest.html" "$REPO_DIR/index.html"
echo "Done."
echo ""

# Step 3: Git push
echo "Step 3: Publishing to GitHub Pages..."
cd "$REPO_DIR"
git add index.html
git commit -m "Dashboard update: $(date '+%Y-%m-%d %H:%M')"
git push

if [ $? -eq 0 ]; then
  echo ""
  echo "======================================"
  echo " Published! Live in ~1 minute at:"
  echo " https://locad-int.github.io/locad-fc-finops-dashboard/"
  echo "======================================"
else
  echo "ERROR: Git push failed. Check your internet connection."
fi

echo ""
read -n 1 -s -r -p "Press any key to close."
