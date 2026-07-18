import json
import os
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "contributions.json")
OUT = os.path.join(BASE, "contrib-heatmap.svg")

with open(DATA) as f:
    data = json.load(f)

days_map = {d["date"]: d["count"] for d in data["days"]}
total = data["total"]
streak = data["current_streak"]
best = data["best_day"]

WEEKS = 53
CELL = 13
GAP = 3
PAD = 20
HEADER_H = 40
FOOTER_H = 40
CELL_W = CELL + GAP
CELL_H = CELL + GAP
SVG_W = PAD * 2 + WEEKS * CELL_W
SVG_H = PAD + HEADER_H + 7 * CELL_H + FOOTER_H

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

today = datetime.now()
start = today - timedelta(weeks=WEEKS - 1)
start = start - timedelta(days=start.weekday())

lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}">')
lines.append('<style>')
lines.append('@keyframes slideIn {')
lines.append('  0% { opacity: 0; transform: translateY(-8px); }')
lines.append('  100% { opacity: 1; transform: translateY(0); }')
lines.append('}')
lines.append('.box { animation: slideIn 0.3s ease-out both; }')
lines.append('.stat { animation: slideIn 0.5s ease-out both; }')
lines.append('</style>')
lines.append(f'<rect width="{SVG_W}" height="{SVG_H}" fill="#0d1117" rx="8"/>')

lines.append(f'<text x="{PAD}" y="35" font-family="monospace" font-size="14" fill="#c9d1d9" font-weight="bold" class="stat" style="animation-delay:0s">{total:,} contributions in the last year</text>')

idx = 0
for w in range(WEEKS):
    for d in range(7):
        date = start + timedelta(weeks=w, days=d)
        ds = date.strftime("%Y-%m-%d")
        count = days_map.get(ds, 0)
        level = min(count, 5)
        color = PALETTE[level]
        x = PAD + w * CELL_W
        y = PAD + HEADER_H + d * CELL_H
        delay = 0.02 * (w + d)
        lines.append(f'  <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{color}" class="box" style="animation-delay:{delay}s"/>')

stats_y = PAD + HEADER_H + 7 * CELL_H + 20
lines.append(f'<text x="{PAD}" y="{stats_y}" font-family="monospace" font-size="12" fill="#8b949e" class="stat" style="animation-delay:1s">Streak: {streak}d · Best: {best["count"]} on {best["date"]}</text>')

legend_x = PAD + 500
lines.append(f'<text x="{legend_x}" y="{stats_y}" font-family="monospace" font-size="11" fill="#8b949e" class="stat" style="animation-delay:1s">Less</text>')
for i, c in enumerate(PALETTE):
    lx = legend_x + 40 + i * (CELL + 4)
    lines.append(f'  <rect x="{lx}" y="{stats_y - 9}" width="{CELL - 2}" height="{CELL - 2}" rx="2" fill="{c}" class="stat" style="animation-delay:{1.2 + i * 0.05}s"/>')
lines.append(f'<text x="{legend_x + 40 + len(PALETTE) * (CELL + 4) + 4}" y="{stats_y}" font-family="monospace" font-size="11" fill="#8b949e" class="stat" style="animation-delay:1s">More</text>')

lines.append('</svg>')

with open(OUT, "w") as f:
    f.write('\n'.join(lines))
print(f"Saved {OUT}")
