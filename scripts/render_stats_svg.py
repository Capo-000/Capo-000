import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRIBS = os.path.join(BASE, "data", "contributions.json")
OUT = os.path.join(BASE, "github-stats.svg")

with open(CONTRIBS) as f:
    data = json.load(f)

total = data["total"]
streak = data["current_streak"]
best = data.get("best_day", {})

W, H = 420, 160
lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
lines.append(f'<rect width="{W}" height="{H}" fill="#0d1117" rx="8"/>')

stats = [
    ("Repos", "1", "#58a6ff"),
    ("Contributions", str(total), "#39d353"),
    ("Streak", f"{streak}d", "#d29922"),
    ("Best Day", str(best.get("count", 0)), "#f78166"),
]

box_w = (W - 40) // len(stats)
for i, (label, value, color) in enumerate(stats):
    x = 20 + i * box_w + box_w // 2
    lines.append(f'<text x="{x}" y="55" text-anchor="middle" font-family="monospace" font-size="24" font-weight="bold" fill="{color}">{value}</text>')
    lines.append(f'<text x="{x}" y="80" text-anchor="middle" font-family="monospace" font-size="11" fill="#8b949e">{label}</text>')

lines.append(f'<text x="20" y="120" font-family="monospace" font-size="11" fill="#8b949e">Account since March 2024</text>')
lines.append(f'<text x="20" y="140" font-family="monospace" font-size="11" fill="#8b949e">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</text>')

lines.append('</svg>')

with open(OUT, "w") as f:
    f.write('\n'.join(lines))
print(f"Saved {OUT}")
