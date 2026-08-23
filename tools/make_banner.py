#!/usr/bin/env python3
"""Generate banner.svg — a self-contained, animated status-board banner for the
GitHub profile. No external services, no fonts fetched: pure SVG + SMIL, so it
renders and animates natively on GitHub (SVG-in-<img>, secure static mode).

    python3 tools/make_banner.py
"""
import math, os

W, H = 1280, 360
VOID, INK, MUT = "#070a0f", "#eef2fb", "#7c88a0"
LINE, AMBER, OK = "#1a2233", "#ffb454", "#46d39a"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

out = []
def add(s): out.append(s)

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="{MONO}" role="img" aria-label="Sourav Kundu — DevOps, SRE and Platform Engineer">')

# ── defs ──────────────────────────────────────────────────────────────────
add('<defs>')
add(f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#0b0f18"/><stop offset="0.55" stop-color="#080b12"/>'
    f'<stop offset="1" stop-color="#05070c"/></linearGradient>')
add(f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
    f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.20"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>')
add(f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
    f'<stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.10"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>')
add(f'<linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.28"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>')
add('</defs>')

# ── ground + grid + glow ──────────────────────────────────────────────────
add(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>')
g = []
for x in range(0, W, 40): g.append(f'M{x} 0V{H}')
for y in range(0, H, 40): g.append(f'M0 {y}H{W}')
add(f'<path d="{"".join(g)}" stroke="{LINE}" stroke-width="1" opacity="0.35"/>')
add(f'<ellipse cx="300" cy="150" rx="520" ry="300" fill="url(#glow)"/>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')

# scanning sweep
add(f'<rect x="-180" y="0" width="180" height="{H}" fill="url(#sweep)">'
    f'<animateTransform attributeName="transform" type="translate" from="-180 0" to="{W} 0" '
    f'dur="7s" repeatCount="indefinite"/></rect>')

# ── top status line ───────────────────────────────────────────────────────
add(f'<circle cx="64" cy="54" r="5" fill="{OK}">'
    f'<animate attributeName="opacity" values="1;0.35;1" dur="1.9s" repeatCount="indefinite"/></circle>')
add(f'<circle cx="64" cy="54" r="5" fill="none" stroke="{OK}" stroke-width="1.5" opacity="0.6">'
    f'<animate attributeName="r" values="5;12;5" dur="1.9s" repeatCount="indefinite"/>'
    f'<animate attributeName="opacity" values="0.6;0;0.6" dur="1.9s" repeatCount="indefinite"/></circle>')
add(f'<text x="80" y="59" font-size="13" letter-spacing="1.5" fill="{MUT}">'
    f'sourav.service &#183; <tspan fill="{OK}">active (running)</tspan>'
    f'<tspan fill="{MUT}">  &#183;  uptime 5y+  &#183;  on call</tspan></text>')

# ── hero: name + role + prompt ────────────────────────────────────────────
add(f'<text x="56" y="168" font-size="66" font-weight="700" letter-spacing="7" fill="{INK}">SOURAV KUNDU</text>')
add(f'<text x="58" y="210" font-size="19.5" letter-spacing="2.5" fill="{AMBER}">'
    f'DevOps &#183; SRE &#183; Platform &amp; Infrastructure Engineer</text>')
# prompt + blinking cursor (cursor is a trailing block glyph, so it auto-positions
# after the text at any font width)
add(f'<text x="58" y="268" font-size="16" letter-spacing="0.5" fill="{MUT}">'
    f'~ $ <tspan fill="{INK}">whoami</tspan> '
    f'<tspan fill="{MUT}">&#8594;</tspan> '
    f'<tspan fill="{INK}">someone who keeps production boring</tspan>'
    f'<tspan fill="{AMBER}"> &#9646;'
    f'<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
    f'dur="1.06s" repeatCount="indefinite"/></tspan></text>')

# ── right panel: latency sparkline (draws itself) ─────────────────────────
X0, X1 = 856, 1224
YT, YB = 78, 150
N = 56
pts = []
for i in range(N):
    t = i/(N-1)
    v = (0.50 + 0.26*math.sin(t*6.3) + 0.15*math.sin(t*17.0+1.0)
         + 0.30*math.exp(-((t-0.66)*9)**2))       # a latency spike near the end
    v = max(0.0, min(1.0, v))
    x = X0 + t*(X1-X0)
    y = YB - v*(YB-YT)
    pts.append((x, y))
# path length (approx) for the draw animation
plen = sum(math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1]) for i in range(N-1))
line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
area = line + f" L{X1} {YB} L{X0} {YB} Z"
add(f'<text x="{X1}" y="56" font-size="12" letter-spacing="2.5" fill="{MUT}" text-anchor="end">LATENCY &#183; p95</text>')
add(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{LINE}" stroke-width="1"/>')
add(f'<path d="{area}" fill="url(#spark)" opacity="0.9"/>')
add(f'<path d="{line}" fill="none" stroke="{AMBER}" stroke-width="2" stroke-linecap="round" '
    f'stroke-linejoin="round" stroke-dasharray="{plen:.0f}" stroke-dashoffset="{plen:.0f}">'
    f'<animate attributeName="stroke-dashoffset" values="{plen:.0f};0;0" keyTimes="0;0.72;1" '
    f'dur="4.8s" repeatCount="indefinite"/></path>')
# moving readout dot at the end of the line
ex, ey = pts[-1]
add(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{AMBER}">'
    f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.7;0.72;1" dur="4.8s" '
    f'repeatCount="indefinite"/></circle>')

# ── right panel: uptime strip ─────────────────────────────────────────────
add(f'<text x="{X0}" y="196" font-size="12" letter-spacing="2.5" fill="{MUT}">UPTIME &#183; 90 DAYS</text>')
sw, gap, sy, sh = 8, 3, 208, 22
n = (X1 - X0 + gap) // (sw + gap)
for i in range(int(n)):
    x = X0 + i*(sw+gap)
    dim = (i % 17 == 16)          # a couple of faint "blips", mostly green
    col = AMBER if dim else OK
    add(f'<rect x="{x}" y="{sy}" width="{sw}" height="{sh}" rx="1.5" fill="{col}" opacity="0.28">'
        f'<animate attributeName="opacity" values="0.24;0.9;0.24" dur="2.6s" '
        f'begin="{i*0.05:.2f}s" repeatCount="indefinite"/></rect>')

# ── footer metrics row ────────────────────────────────────────────────────
fy = 312
add(f'<line x1="56" y1="{fy-22}" x2="{W-56}" y2="{fy-22}" stroke="{LINE}" stroke-width="1"/>')
metrics = [("REGIONS", "AP &#183; EU"), ("STACK", "Go &#183; Terraform &#183; k8s"),
           ("EDGE", "Cloudflare"), ("BUILT", "tools when they don&#8217;t exist")]
mx = 56
for label, val in metrics:
    add(f'<text x="{mx}" y="{fy}" font-size="11" letter-spacing="2" fill="{MUT}">{label}</text>')
    add(f'<text x="{mx}" y="{fy+18}" font-size="13.5" fill="{INK}">{val}</text>')
    mx += 300

add('</svg>')

svg = "\n".join(out) + "\n"
path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banner.svg")
open(path, "w", encoding="utf-8").write(svg)
print(f"wrote {path}  ({len(svg)} bytes)")
