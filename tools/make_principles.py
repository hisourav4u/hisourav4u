#!/usr/bin/env python3
"""Generate principles.svg — a grid of principle cards (mono eyebrow -> headline
-> serif qualifier), echoing the portfolio overview. Self-contained, cards are
always visible (a scan sweep is the only motion, so content never depends on
animation playing)."""
import os

W, H = 1280, 500
VOID, INK, MUT = "#070a0f", "#eef2fb", "#8792a8"
LINE, AMBER, OK = "#1a2233", "#ffb454", "#46d39a"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SERIF = "Iowan Old Style, Georgia, 'Times New Roman', serif"

CARDS = [
 ("01","IN PRODUCTION","Five years, kept boring",
   ["The best infrastructure is the","kind nobody has to think about."]),
 ("02","WHAT I OWN","The entire cloud estate",
   ["Not one team's slice — six live","brands, end to end."]),
 ("03","HOW WORK FINDS ME","No ticket required",
   ["If I see it, I build it. I don't","wait to be assigned."]),
 ("04","WHAT DONE MEANS","End to end, no ifs",
   ["Shipped, observed, and rehearsed","for the day it breaks."]),
 ("05","WHEN IT DOESN'T EXIST","I build the tool",
   ["Paging, DNS checks, escalation —","self-hosted, not licensed."]),
 ("06","BLAST RADIUS","Plan, then apply",
   ["Reversible by default. The 2am","version has to be safe too."]),
]

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
out=[]
def add(s): out.append(s)

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="{MONO}" role="img" aria-label="How I work — principles">')
add('<defs>')
add(f'<linearGradient id="bg2" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#0a0e16"/><stop offset="1" stop-color="#06080d"/></linearGradient>')
add(f'<linearGradient id="sweep2" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
    f'<stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.06"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>')
add('</defs>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg2)"/>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
# section header
add(f'<text x="48" y="56" font-size="13" letter-spacing="3" fill="{MUT}">'
    f'<tspan fill="{AMBER}">//</tspan> HOW I WORK</text>')
add(f'<text x="{W-48}" y="56" font-size="12" letter-spacing="2" fill="{MUT}" text-anchor="end">'
    f'principles.d &#183; 6 loaded</text>')
# scan sweep across the cards
add(f'<rect x="-200" y="76" width="200" height="{H-124}" fill="url(#sweep2)">'
    f'<animateTransform attributeName="transform" type="translate" from="-200 0" to="{W} 0" '
    f'dur="8s" repeatCount="indefinite"/></rect>')

# card grid
M=48; top=92; gap=24
cw=(W-2*M-2*gap)/3; ch=168
for i,(idx,eye,head,ql) in enumerate(CARDS):
    col=i%3; row=i//3
    x=M+col*(cw+gap); y=top+row*(ch+gap)
    add(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{ch}" rx="12" fill="#0c111b" '
        f'stroke="{LINE}" stroke-width="1.25"/>')
    add(f'<text x="{x+cw-18:.0f}" y="{y+30}" font-size="12" fill="{LINE if False else "#33405c"}" '
        f'text-anchor="end" letter-spacing="1">{idx}</text>')
    add(f'<text x="{x+22:.0f}" y="{y+34}" font-size="11" letter-spacing="2.5" fill="{MUT}">{esc(eye)}</text>')
    add(f'<text x="{x+22:.0f}" y="{y+72}" font-size="22" font-weight="700" fill="{INK}">{esc(head)}</text>')
    add(f'<rect x="{x+22:.0f}" y="{y+84}" width="34" height="2.5" fill="{AMBER}"/>')
    yy=y+118
    for line in ql:
        add(f'<text x="{x+22:.0f}" y="{yy}" font-size="14.5" font-family="{SERIF}" font-style="italic" '
            f'fill="#aeb7c9">{esc(line)}</text>')
        yy+=23
add('</svg>')

svg="\n".join(out)+"\n"
path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"principles.svg")
open(path,"w",encoding="utf-8").write(svg)
print(f"wrote {path} ({len(svg)} bytes)")
