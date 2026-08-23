#!/usr/bin/env python3
"""Generate the remaining profile panels as self-contained SVG:
  experience.svg  — a proportional career timeline
  stack.svg       — the toolchain, grouped
  assets/hdr_*.svg    — slim section headers
  assets/card_*.svg   — one clickable card per project (wrapped in a link in the README)
  assets/link_*.svg   — external link buttons
No external services; content is always visible (motion is decorative only)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets"); os.makedirs(ASSETS, exist_ok=True)

INK, MUT = "#eef2fb", "#8792a8"
LINE, AMBER, OK, BLUE = "#1a2233", "#ffb454", "#46d39a", "#6fb0ff"
PANEL = "#0c111b"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SERIF = "Iowan Old Style, Georgia, 'Times New Roman', serif"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def bgdefs(pid):
    return (f'<linearGradient id="{pid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#0a0e16"/><stop offset="1" stop-color="#06080d"/></linearGradient>')
def frame(w,h,pid):
    return (f'<rect width="{w}" height="{h}" rx="16" fill="url(#{pid})"/>'
            f'<rect width="{w}" height="{h}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
def svg_open(w,h,label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{MONO}" role="img" aria-label="{esc(label)}">')
def write(name, body): open(os.path.join(ROOT,name),"w",encoding="utf-8").write(body+"\n"); print("wrote",name)
def writea(name, body): open(os.path.join(ASSETS,name),"w",encoding="utf-8").write(body+"\n"); print("wrote assets/"+name)

# ── EXPERIENCE ──────────────────────────────────────────────────────────────
def experience():
    W,H=1280,270
    o=[svg_open(W,H,"Experience timeline: Momentum Group, Warner Bros Discovery, Parallel Wireless"),
       '<defs>'+bgdefs("bge")+'</defs>',frame(W,H,"bge")]
    o.append(f'<text x="48" y="52" font-size="13" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> EXPERIENCE</text>')
    o.append(f'<text x="{W-48}" y="52" font-size="12" letter-spacing="2" fill="{MUT}" text-anchor="end">5y+ &#183; continuing</text>')
    M=56; start=2021.0; now=2026.67
    def X(t): return M + (t-start)/(now-start)*(W-2*M)
    # year ticks
    for yr in range(2021,2027):
        x=X(yr)
        o.append(f'<line x1="{x:.0f}" y1="76" x2="{x:.0f}" y2="228" stroke="{LINE}" stroke-width="1" opacity="0.6"/>')
        o.append(f'<text x="{x:.0f}" y="250" font-size="11" fill="{MUT}" text-anchor="middle">{yr}</text>')
    roles=[
      ("Lead DevOps / Infrastructure Engineer","Momentum Group",2025.25,now,AMBER,True,"APR 2025 — NOW"),
      ("Senior DevOps Engineer","Warner Bros. Discovery",2021.54,2025.0,INK,False,"JUL 2021 — JAN 2025"),
      ("R&D Quality Engineer — Automation","Parallel Wireless",2021.0,2021.54,MUT,False,"JAN — JUL 2021"),
    ]
    lane=[92,140,188]
    for (role,org,a,b,col,cur,dates),ly in zip(roles,lane):
        x1,x2=X(a),X(b); bw=max(x2-x1,10)
        o.append(f'<rect x="{x1:.0f}" y="{ly}" width="{bw:.0f}" height="30" rx="6" fill="{col}" opacity="{0.9 if cur else 0.22}"/>')
        if cur:
            o.append(f'<rect x="{x1:.0f}" y="{ly}" width="{bw:.0f}" height="30" rx="6" fill="none" stroke="{AMBER}" stroke-width="1.5"/>')
            o.append(f'<circle cx="{x2:.0f}" cy="{ly+15}" r="5" fill="{AMBER}"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>')
            o.append(f'<circle cx="{x2:.0f}" cy="{ly+15}" r="5" fill="none" stroke="{AMBER}" stroke-width="1.5"><animate attributeName="r" values="5;13;5" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="1.8s" repeatCount="indefinite"/></circle>')
        tcol = "#06080d" if cur else INK
        o.append(f'<text x="{x1+12:.0f}" y="{ly+20}" font-size="12.5" font-weight="700" fill="{tcol}">{esc(org)}</text>')
        o.append(f'<text x="{x1:.0f}" y="{ly-8}" font-size="11.5" fill="{MUT if not cur else AMBER}">{esc(role)}  &#183;  <tspan fill="{MUT}">{dates}</tspan></text>')
    o.append('</svg>')
    write("experience.svg","\n".join(o))

# ── STACK ───────────────────────────────────────────────────────────────────
def stack():
    W,H=1280,428
    groups=[("LANGUAGES",[("Go",1),("Python",1),("Bash",0)]),
            ("INFRA AS CODE",[("Terraform",1),("Terragrunt",1)]),
            ("CLOUD",[("AWS",1),("ECS",0),("EKS",0),("Lambda",0)]),
            ("EDGE",[("Cloudflare",1),("Workers",0),("WAF",0)]),
            ("ORCHESTRATION",[("Kubernetes",1),("Docker",0)]),
            ("CI / CD",[("GitHub Actions",1),("Spinnaker",0)]),
            ("OBSERVABILITY",[("OpenTelemetry",1),("SigNoz",0),("Prometheus",0)]),
            ("DATA",[("PostgreSQL",1)])]
    o=[svg_open(W,H,"Stack: languages, IaC, cloud, edge, orchestration, CI/CD, observability, data"),
       '<defs>'+bgdefs("bgs")+'</defs>',frame(W,H,"bgs")]
    o.append(f'<text x="48" y="52" font-size="13" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> STACK</text>')
    o.append(f'<text x="{W-48}" y="52" font-size="12" letter-spacing="2" fill="{MUT}" text-anchor="end">amber = daily driver</text>')
    y=88; labelw=220
    for gname,chips in groups:
        o.append(f'<text x="48" y="{y+20}" font-size="11.5" letter-spacing="2" fill="{MUT}">{gname}</text>')
        x=48+labelw
        for name,daily in chips:
            cw=len(name)*8.4+26
            bd = AMBER if daily else LINE
            tx = INK
            o.append(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="28" rx="7" fill="#0e1420" stroke="{bd}" stroke-width="1.25"/>')
            o.append(f'<text x="{x+cw/2:.0f}" y="{y+19}" font-size="13" fill="{tx}" text-anchor="middle">{esc(name)}</text>')
            x+=cw+10
        y+=39
    o.append('</svg>')
    write("stack.svg","\n".join(o))

# ── section header strips ────────────────────────────────────────────────────
def header(slug,label,meta):
    W,H=1280,58
    o=[svg_open(W,H,label),'<defs>'+bgdefs("bgh_"+slug)+'</defs>',frame(W,H,"bgh_"+slug)]
    o.append(f'<text x="40" y="37" font-size="13" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> {esc(label)}</text>')
    o.append(f'<text x="{W-40}" y="37" font-size="12" letter-spacing="2" fill="{MUT}" text-anchor="end">{esc(meta)}</text>')
    o.append('</svg>')
    writea(f"hdr_{slug}.svg","\n".join(o))

# ── project cards (clickable) ────────────────────────────────────────────────
def card(slug,name,tag,tagline,accent):
    W,H=440,132
    o=[svg_open(W,H,f"{name} — {tagline}"),'<defs>'+bgdefs("bgc_"+slug)+'</defs>']
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.25"/>')
    o.append(f'<rect x="0" y="10" width="5" height="{H-20}" rx="2.5" fill="{accent}"/>')
    o.append(f'<text x="26" y="46" font-size="21" font-weight="700" fill="{INK}">{esc(name)}</text>')
    # type chip top-right
    cw=len(tag)*7.2+22
    o.append(f'<rect x="{W-26-cw:.0f}" y="26" width="{cw:.0f}" height="24" rx="7" fill="#0e1420" stroke="{LINE}"/>')
    o.append(f'<text x="{W-26-cw/2:.0f}" y="42" font-size="11" fill="{MUT}" text-anchor="middle">{esc(tag)}</text>')
    o.append(f'<text x="26" y="80" font-size="14.5" font-family="{SERIF}" font-style="italic" fill="#aeb7c9">{esc(tagline)}</text>')
    o.append(f'<text x="26" y="112" font-size="11.5" letter-spacing="1.5" fill="{accent}">open &#8594;</text>')
    o.append('</svg>')
    writea(f"card_{slug}.svg","\n".join(o))

# ── link buttons (clickable) ─────────────────────────────────────────────────
def linkbtn(slug,label,sub,accent):
    W,H=413,72
    o=[svg_open(W,H,f"{label} — {sub}"),f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}"/>',
       f'<rect width="{W}" height="{H}" rx="12" fill="none" stroke="{LINE}" stroke-width="1.25"/>',
       f'<rect x="0" y="9" width="5" height="{H-18}" rx="2.5" fill="{accent}"/>',
       f'<text x="24" y="32" font-size="12" letter-spacing="2.5" fill="{MUT}">{esc(label)}</text>',
       f'<text x="24" y="54" font-size="15" fill="{INK}">{esc(sub)}</text>',
       f'<text x="{W-22}" y="30" font-size="15" fill="{accent}" text-anchor="end">&#8599;</text>','</svg>']
    writea(f"link_{slug}.svg","\n".join(o))

experience(); stack()
header("built","THINGS WITH A FACE ON THEM","self-contained · no dependencies")
header("elsewhere","ELSEWHERE","the rest of me")

CARDS=[
 ("minutes","Minutes","macOS · Swift","meetings → notes, on-device",AMBER),
 ("bulwark","Bulwark","Chrome · MV3","ad, popup & redirect blocker",AMBER),
 ("clipboardmanager","ClipboardManager","macOS · Swift","clipboard history, bound to ⌘⌃V",AMBER),
 ("blobtodo","BlobTodo","macOS · SwiftUI","a floating todo widget",AMBER),
 ("meetingreminder","MeetingReminder","macOS · Swift","a banner before every meeting",AMBER),
 ("tabdeck","TabDeck","Chrome · MV3","manual tab grouping that stays",AMBER),
 ("solarsystem","Orrery","WebGL2","an explorable Solar System",OK),
 ("humananatomy","Corpus","WebGL2","a dissectable human body",OK),
 ("cpuanatomy","Silicon","WebGL2","an anatomy of a CPU",OK),
 ("winsim","WinSim","vanilla JS","Windows XP & Vista in a tab",OK),
 ("voidgraze","VoidGraze","Canvas","a bullet-hell scored on uptime",OK),
 ("passportsheet","Passport Sheet","Canvas","4×6 passport-photo print tool",OK),
]
for slug,name,tag,tl,ac in CARDS: card(slug,name,tag,tl,ac)

linkbtn("portfolio","PORTFOLIO","souravkundu.dev",AMBER)
linkbtn("labs","LABS","souravkundu.dev/labs",OK)
linkbtn("linkedin","LINKEDIN","in/souravkundu1998",BLUE)
print("done")
