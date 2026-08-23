#!/usr/bin/env python3
"""principles.svg — principle cards, designed at ~940px so text is natural size."""
import os
W, H = 940, 672
INK, MUT, LINE, AMBER = "#eef2fb", "#8792a8", "#1a2233", "#ffb454"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SERIF = "Iowan Old Style, Georgia, 'Times New Roman', serif"
CARDS=[
 ("01","IN PRODUCTION","Five years, kept boring",["The best infrastructure is the","kind nobody has to think about."]),
 ("02","WHAT I OWN","The entire cloud estate",["Not one team's slice — six live","brands, end to end."]),
 ("03","HOW WORK FINDS ME","No ticket required",["If I see it, I build it. I don't","wait to be assigned."]),
 ("04","WHAT DONE MEANS","End to end, no ifs",["Shipped, observed, and rehearsed","for the day it breaks."]),
 ("05","WHEN IT DOESN'T EXIST","I build the tool",["Paging, DNS checks, escalation —","self-hosted, not licensed."]),
 ("06","BLAST RADIUS","Plan, then apply",["Reversible by default. The 2am","version has to be safe too."]),
]
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
o=[]; add=o.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="How I work — principles">')
add('<defs><linearGradient id="bg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0e16"/><stop offset="1" stop-color="#06080d"/></linearGradient>'
    f'<linearGradient id="sw2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.06"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient></defs>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg2)"/><rect width="{W}" height="{H}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
add(f'<text x="40" y="50" font-size="15" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> HOW I WORK</text>')
add(f'<text x="{W-40}" y="50" font-size="13" letter-spacing="2" fill="{MUT}" text-anchor="end">principles.d &#183; 6 loaded</text>')
add(f'<rect x="-180" y="70" width="180" height="{H-110}" fill="url(#sw2)"><animateTransform attributeName="transform" type="translate" from="-180 0" to="{W} 0" dur="8s" repeatCount="indefinite"/></rect>')
M=40; top=86; gap=20; cw=(W-2*M-gap)/2; ch=168   # 2 columns so headlines fit
for i,(idx,eye,head,ql) in enumerate(CARDS):
    x=M+(i%2)*(cw+gap); y=top+(i//2)*(ch+20)
    add(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="{ch}" rx="12" fill="#0c111b" stroke="{LINE}" stroke-width="1.25"/>')
    add(f'<text x="{x+cw-16:.0f}" y="{y+30}" font-size="13" fill="#33405c" text-anchor="end">{idx}</text>')
    add(f'<text x="{x+22:.0f}" y="{y+36}" font-size="13" letter-spacing="2" fill="{MUT}">{esc(eye)}</text>')
    add(f'<text x="{x+22:.0f}" y="{y+76}" font-size="24" font-weight="700" fill="{INK}">{esc(head)}</text>')
    add(f'<rect x="{x+22:.0f}" y="{y+88}" width="34" height="2.5" fill="{AMBER}"/>')
    yy=y+124
    for ln in ql:
        add(f'<text x="{x+22:.0f}" y="{yy}" font-size="15.5" font-family="{SERIF}" font-style="italic" fill="#aeb7c9">{esc(ln)}</text>'); yy+=25
add('</svg>')
open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"principles.svg"),"w").write("\n".join(o)+"\n")
print("principles.svg",W,"x",H)
