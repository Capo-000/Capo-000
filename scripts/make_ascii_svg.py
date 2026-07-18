from PIL import Image
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "source-prepped.png")
OUT = os.path.join(BASE, "capo-ascii.svg")
W, H = 100, 53
RAMP = " .`:-=+*cs#%@"

img = Image.open(SRC).convert("L")
img = img.resize((W, H), Image.LANCZOS)
pixels = list(img.getdata())

chars = []
for p in pixels:
    idx = int((255 - p) / 255 * (len(RAMP) - 1))
    chars.append(RAMP[idx])
chars = [chars[i * W:(i + 1) * W] for i in range(H)]

font_size = 8
char_w = font_size * 0.6
char_h = font_size * 1.2
svg_w = W * char_w
svg_h = H * char_h

lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w:.0f}" height="{svg_h:.0f}" viewBox="0 0 {svg_w:.0f} {svg_h:.0f}">')
lines.append('<style>')
lines.append('@keyframes typeRow {')
lines.append('  0% { clip-path: inset(0 100% 0 0); }')
lines.append('  100% { clip-path: inset(0 0 0 0); }')
lines.append('}')
lines.append('@keyframes cursor {')
lines.append('  0%, 90% { opacity: 1; }')
lines.append('  100% { opacity: 0; }')
lines.append('}')
lines.append('.row { animation: typeRow 0.6s ease-out both; }')
lines.append('</style>')
lines.append(f'<rect width="{svg_w:.0f}" height="{svg_h:.0f}" fill="#0d1117"/>')
lines.append(f'<text x="0" y="0" font-family="monospace" font-size="{font_size}" fill="#c9d1d9" font-weight="bold">')

for r, row in enumerate(chars):
    delay = r * 0.04
    y = (r + 1) * char_h
    line_chars = ''.join(row)
    lines.append(f'  <tspan x="0" dy="{char_h}" class="row" style="animation-delay: {delay}s">{line_chars}</tspan>')

lines.append('</text>')
lines.append('</svg>')

with open(OUT, 'w') as f:
    f.write('\n'.join(lines))
print(f"Saved {OUT}")
