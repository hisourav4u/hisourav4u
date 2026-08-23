#!/usr/bin/env python3
"""banner.svg — animated status-board hero. Designed at ~940px (GitHub's README
render width) so text displays at natural size, not shrunk. Self-contained SVG."""
import math, os
W, H = 940, 300
INK, MUT, LINE, AMBER, OK = "#eef2fb", "#8792a8", "#1a2233", "#ffb454", "#46d39a"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
o=[]; add=o.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="{MONO}" role="img" aria-label="Sourav Kundu — DevOps, SRE and Platform Engineer">')
add('<defs>'
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0f18"/>'
    f'<stop offset="0.55" stop-color="#080b12"/><stop offset="1" stop-color="#05070c"/></linearGradient>'
    f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.18"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
    f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
    f'<stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.09"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
    f'<linearGradient id="spark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.3"/>'
    f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>')
g=[f'M{x} 0V{H}' for x in range(0,W,40)]+[f'M0 {y}H{W}' for y in range(0,H,40)]
add(f'<path d="{"".join(g)}" stroke="{LINE}" stroke-width="1" opacity="0.35"/>')
add(f'<ellipse cx="230" cy="130" rx="440" ry="260" fill="url(#glow)"/>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
add(f'<rect x="-160" y="0" width="160" height="{H}" fill="url(#sweep)">'
    f'<animateTransform attributeName="transform" type="translate" from="-160 0" to="{W} 0" dur="7s" repeatCount="indefinite"/></rect>')
# status
add(f'<circle cx="52" cy="48" r="5" fill="{OK}"><animate attributeName="opacity" values="1;0.35;1" dur="1.9s" repeatCount="indefinite"/></circle>')
add(f'<circle cx="52" cy="48" r="5" fill="none" stroke="{OK}" stroke-width="1.5"><animate attributeName="r" values="5;12;5" dur="1.9s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0;0.6" dur="1.9s" repeatCount="indefinite"/></circle>')
add(f'<text x="68" y="53" font-size="14" letter-spacing="1" fill="{MUT}">sourav.service &#183; <tspan fill="{OK}">active (running)</tspan><tspan fill="{MUT}">  &#183;  uptime 5y+  &#183;  on call</tspan></text>')
# hero
add(f'<text x="44" y="136" font-size="56" font-weight="700" letter-spacing="5" fill="{INK}">SOURAV KUNDU</text>')
add(f'<text x="46" y="174" font-size="18.5" letter-spacing="1.5" fill="{AMBER}">DevOps &#183; SRE &#183; Platform &amp; Infrastructure Engineer</text>')
add(f'<text x="46" y="222" font-size="15.5" fill="{MUT}">~ $ <tspan fill="{INK}">whoami</tspan> <tspan fill="{MUT}">&#8594;</tspan> '
    f'<tspan fill="{INK}">keeps production boring</tspan><tspan fill="{AMBER}"> &#9646;'
    f'<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.06s" repeatCount="indefinite"/></tspan></text>')
# right: sparkline
X0,X1,YT,YB=628,896,70,128; N=48
pts=[]
for i in range(N):
    t=i/(N-1); v=0.5+0.26*math.sin(t*6.3)+0.15*math.sin(t*17+1)+0.3*math.exp(-((t-0.66)*9)**2)
    v=max(0,min(1,v)); pts.append((X0+t*(X1-X0), YB-v*(YB-YT)))
plen=sum(math.hypot(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1]) for i in range(N-1))
line="M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts); area=line+f" L{X1} {YB} L{X0} {YB} Z"
add(f'<text x="{X1}" y="52" font-size="12.5" letter-spacing="2" fill="{MUT}" text-anchor="end">LATENCY &#183; p95</text>')
add(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="{LINE}"/>')
add(f'<path d="{area}" fill="url(#spark)"/>')
add(f'<path d="{line}" fill="none" stroke="{AMBER}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    f'stroke-dasharray="{plen:.0f}" stroke-dashoffset="{plen:.0f}"><animate attributeName="stroke-dashoffset" '
    f'values="{plen:.0f};0;0" keyTimes="0;0.72;1" dur="4.8s" repeatCount="indefinite"/></path>')
# uptime strip
add(f'<text x="{X0}" y="162" font-size="12.5" letter-spacing="2" fill="{MUT}">UPTIME &#183; 90 DAYS</text>')
sw,gap,sy,sh=7,3,172,20; n=int((X1-X0+gap)//(sw+gap))
for i in range(n):
    col=AMBER if i%17==16 else OK
    add(f'<rect x="{X0+i*(sw+gap)}" y="{sy}" width="{sw}" height="{sh}" rx="1.5" fill="{col}" opacity="0.28">'
        f'<animate attributeName="opacity" values="0.24;0.9;0.24" dur="2.6s" begin="{i*0.05:.2f}s" repeatCount="indefinite"/></rect>')
# footer
add(f'<line x1="44" y1="248" x2="{W-44}" y2="248" stroke="{LINE}"/>')
for i,(lab,val) in enumerate([("REGIONS","AP &#183; EU"),("STACK","Go &#183; Terraform &#183; k8s"),
                              ("EDGE","Cloudflare"),("BUILT","when it doesn&#8217;t exist")]):
    mx=44+i*225
    add(f'<text x="{mx}" y="272" font-size="11.5" letter-spacing="2" fill="{MUT}">{lab}</text>')
    add(f'<text x="{mx}" y="290" font-size="14" fill="{INK}">{val}</text>')
add('</svg>')
open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"banner.svg"),"w").write("\n".join(o)+"\n")
print("banner.svg", W,"x",H)
