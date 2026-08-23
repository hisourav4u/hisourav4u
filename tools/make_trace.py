#!/usr/bin/env python3
"""trace.svg — a request travelling the full path, designed at ~940px."""
import os
W, H = 940, 210
INK, MUT, LINE, AMBER, OK = "#eef2fb", "#8792a8", "#1a2233", "#ffb454", "#46d39a"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SPANS=["dns.resolve","edge.terminate","net.route","compute.schedule","app.run","data.query","telemetry.emit"]
DUR=5.0; X0,X1,RY=88,852,116; n=len(SPANS)
xs=[X0+i*(X1-X0)/(n-1) for i in range(n)]
o=[]; add=o.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="A request end to end: dns, edge, network, compute, app, data, telemetry">')
add('<defs><linearGradient id="bg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0e16"/><stop offset="1" stop-color="#06080d"/></linearGradient>'
    f'<radialGradient id="pk" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.9"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient></defs>')
add(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg3)"/><rect width="{W}" height="{H}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
add(f'<text x="40" y="48" font-size="15" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> A REQUEST, END TO END</text>')
add(f'<text x="{W-40}" y="48" font-size="13" letter-spacing="1" fill="{MUT}" text-anchor="end">GET https://brand/ &#8594; <tspan fill="{OK}">200 OK</tspan></text>')
add(f'<line x1="{X0}" y1="{RY}" x2="{X1}" y2="{RY}" stroke="{LINE}" stroke-width="2"/>')
add(f'<line x1="{X0}" y1="{RY}" x2="{X0}" y2="{RY}" stroke="{AMBER}" stroke-width="2" opacity="0.55"><animate attributeName="x2" values="{X0};{X1};{X1}" keyTimes="0;0.9;1" dur="{DUR}s" repeatCount="indefinite"/></line>')
for i,(x,span) in enumerate(zip(xs,SPANS)):
    f=i/(n-1); a=max(0,f-0.03); b=min(1,f+0.03); kt=f"0;{a:.3f};{f:.3f};{b:.3f};1"
    add(f'<circle cx="{x:.0f}" cy="{RY}" r="6.5" fill="#0c111b" stroke="{MUT}" stroke-width="1.5">'
        f'<animate attributeName="fill" values="#0c111b;#0c111b;{AMBER};#0c111b;#0c111b" keyTimes="{kt}" dur="{DUR}s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke" values="{MUT};{MUT};{AMBER};{MUT};{MUT}" keyTimes="{kt}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    add(f'<text x="{x:.0f}" y="{RY+32}" font-size="12.5" fill="{MUT}" text-anchor="middle">{span.replace("&","&amp;")}</text>')
add(f'<circle cy="{RY}" r="15" fill="url(#pk)"><animate attributeName="cx" values="{X0};{X1};{X1}" keyTimes="0;0.9;1" dur="{DUR}s" repeatCount="indefinite"/></circle>')
add(f'<circle cy="{RY}" r="4.5" fill="#fff2dc" stroke="{AMBER}" stroke-width="1.5"><animate attributeName="cx" values="{X0};{X1};{X1}" keyTimes="0;0.9;1" dur="{DUR}s" repeatCount="indefinite"/></circle>')
add(f'<text x="{W/2:.0f}" y="{H-20}" font-size="14" fill="{MUT}" text-anchor="middle" font-family="Iowan Old Style, Georgia, serif" font-style="italic">'
    f'&#8220;a request that crossed all of this — and the person who made it never thought about any of it.&#8221;</text>')
add('</svg>')
open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"trace.svg"),"w").write("\n".join(o)+"\n")
print("trace.svg",W,"x",H)
