import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "info-card.svg")
W, H = 490, 400
STATIC = os.getenv("STATIC", "") == "1"

lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
lines.append('<style>')
if not STATIC:
    lines.append('@keyframes fadeSlide {')
    lines.append('  0% { opacity: 0; transform: translateY(8px); }')
    lines.append('  100% { opacity: 1; transform: translateY(0); }')
    lines.append('}')
    lines.append('.line { animation: fadeSlide 0.4s ease-out both; }')
lines.append('</style>')
lines.append(f'<rect width="{W}" height="{H}" fill="#0d1117" rx="8"/>')

title = "+--[capo@github]---+"
if STATIC:
    lines.append(f'<text x="20" y="30" font-family="monospace" font-size="14" fill="#58a6ff" font-weight="bold">{title}</text>')
else:
    lines.append(f'<text x="20" y="30" font-family="monospace" font-size="14" fill="#58a6ff" font-weight="bold" class="line" style="animation-delay:0s">{title}</text>')

rows = [
    (0.1, "cyan",   " |-- Now",    "Penetration Tester / Threat Intel"),
    (0.2, "green",  " |-- Prev",   "Security Researcher"),
    (0.3, "yellow", " |-- Stack",  "Python | Go | Rust | KQL | PowerShell"),
    (0.4, "magenta"," |-- Tools",  "Burp | BloodHound | CobaltStrike | Metasploit"),
    (0.5, "red",    " |-- Focus",  "Threat Intel | Adversary Emulation | DFIR"),
    (0.6, "blue",   " |-- Certs",  "OSCP | PNPT | CRTO"),
    (0.7, "cyan",   " +-- Links",  "capo.io | @capo_00"),
]

for delay, color, label, value in rows:
    cls = f' class="line" style="animation-delay:{delay}s"' if not STATIC else ''
    i = rows.index((delay, color, label, value))
    y = 50 + i * 38
    lines.append(f'  <text x="20" y="{y}" font-family="monospace" font-size="13" fill="#{color}"{cls}>{label}  </text>')
    lines.append(f'  <text x="200" y="{y}" font-family="monospace" font-size="13" fill="#c9d1d9"{cls}>{value}</text>')

lines.append('</svg>')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Saved {OUT}")
