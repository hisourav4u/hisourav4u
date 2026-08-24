#!/usr/bin/env python3
"""Content panels at ~940px render width (natural text size):
  experience.svg (legend + timeline, never overflows), stack.svg,
  assets/hdr_*.svg, assets/card_*.svg (2-col, ~1:1), assets/link_*.svg."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS=os.path.join(ROOT,"assets"); os.makedirs(ASSETS,exist_ok=True)
INK, MUT, LINE, AMBER, OK, BLUE = "#eef2fb","#8792a8","#1a2233","#ffb454","#46d39a","#6fb0ff"
PANEL="#0c111b"
MONO="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
SERIF="Iowan Old Style, Georgia, 'Times New Roman', serif"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
def bg(pid): return (f'<linearGradient id="{pid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0e16"/><stop offset="1" stop-color="#06080d"/></linearGradient>')
def frame(w,h,pid): return f'<rect width="{w}" height="{h}" rx="16" fill="url(#{pid})"/><rect width="{w}" height="{h}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
def head(w,h,label): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{MONO}" role="img" aria-label="{esc(label)}">'
def W(name,s): open(os.path.join(ROOT,name),"w").write(s+"\n"); print(name)
def A(name,s): open(os.path.join(ASSETS,name),"w").write(s+"\n"); print("assets/"+name)

# ── EXPERIENCE: legend (left) + timeline (right) ──────────────────────────────
def experience():
    w,h=940,300
    o=[head(w,h,"Experience: Momentum Group, Warner Bros Discovery, Parallel Wireless"),'<defs>'+bg("bge")+'</defs>',frame(w,h,"bge")]
    o.append(f'<text x="40" y="50" font-size="13.5" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> EXPERIENCE</text>')
    o.append(f'<text x="{w-40}" y="50" font-size="11.5" letter-spacing="2" fill="{MUT}" text-anchor="end">5y+ &#183; continuing</text>')
    roles=[("Momentum Group","Lead DevOps / Infrastructure Engineer","APR 2025 — NOW",2025.25,2026.67,AMBER,True),
           ("Warner Bros. Discovery","Senior DevOps Engineer","JUL 2021 — JAN 2025",2021.54,2025.0,INK,False),
           ("Parallel Wireless","R&D Quality Engineer — Automation","JAN — JUL 2021",2021.0,2021.54,MUT,False)]
    ey=[96,168,240]
    # legend
    for (org,role,dates,a,b,col,cur),y in zip(roles,ey):
        o.append(f'<rect x="40" y="{y-12}" width="12" height="12" rx="2" fill="{col}"/>')
        o.append(f'<text x="62" y="{y}" font-size="16" font-weight="700" fill="{INK}">{esc(org)}</text>')
        o.append(f'<text x="62" y="{y+21}" font-size="12" fill="{AMBER if cur else MUT}">{esc(role)}</text>')
        o.append(f'<text x="62" y="{y+40}" font-size="11.5" fill="{MUT}">{dates}</text>')
    # timeline
    TX0,TX1=520,900; start,now=2021.0,2026.67
    def X(t): return TX0+(t-start)/(now-start)*(TX1-TX0)
    for yr in range(2021,2027):
        x=X(yr); o.append(f'<line x1="{x:.0f}" y1="78" x2="{x:.0f}" y2="262" stroke="{LINE}" opacity="0.6"/>')
        o.append(f'<text x="{x:.0f}" y="282" font-size="11" fill="{MUT}" text-anchor="middle">{yr}</text>')
    for (org,role,dates,a,b,col,cur),y in zip(roles,ey):
        x1,x2=X(a),X(b); bw=max(x2-x1,8)
        o.append(f'<rect x="{x1:.0f}" y="{y-24}" width="{bw:.0f}" height="30" rx="6" fill="{col}" opacity="{0.9 if cur else 0.28}"/>')
        if cur:
            o.append(f'<rect x="{x1:.0f}" y="{y-24}" width="{bw:.0f}" height="30" rx="6" fill="none" stroke="{AMBER}" stroke-width="1.5"/>')
            o.append(f'<circle cx="{x2:.0f}" cy="{y-9}" r="5" fill="{AMBER}"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>')
            o.append(f'<circle cx="{x2:.0f}" cy="{y-9}" r="5" fill="none" stroke="{AMBER}" stroke-width="1.5"><animate attributeName="r" values="5;13;5" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="1.8s" repeatCount="indefinite"/></circle>')
    o.append('</svg>'); W("experience.svg","\n".join(o))

# ── STACK ─────────────────────────────────────────────────────────────────────
def stack():
    groups=[("LANGUAGES",[("Go",1),("Python",1),("Bash",0)]),("INFRA AS CODE",[("Terraform",1),("Terragrunt",1)]),
            ("CLOUD",[("AWS",1),("ECS",0),("EKS",0),("Lambda",0)]),("EDGE",[("Cloudflare",1),("Workers",0),("WAF",0)]),
            ("ORCHESTRATION",[("Kubernetes",1),("Docker",0)]),("CI / CD",[("GitHub Actions",1),("Spinnaker",0)]),
            ("OBSERVABILITY",[("OpenTelemetry",1),("SigNoz",0),("Prometheus",0)]),("DATA",[("PostgreSQL",1)])]
    w=940; rows=len(groups); y0=88; step=46; h=y0+rows*step-10
    o=[head(w,h,"Stack: languages, IaC, cloud, edge, orchestration, CI/CD, observability, data"),'<defs>'+bg("bgs")+'</defs>',frame(w,h,"bgs")]
    o.append(f'<text x="40" y="50" font-size="13.5" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> STACK</text>')
    o.append(f'<text x="{w-40}" y="50" font-size="11.5" letter-spacing="2" fill="{MUT}" text-anchor="end">amber = daily driver</text>')
    y=y0
    for gname,chips in groups:
        o.append(f'<text x="40" y="{y+22}" font-size="11.5" letter-spacing="1.5" fill="{MUT}">{gname}</text>')
        x=250
        for name,daily in chips:
            cw=len(name)*9.4+30; bd=AMBER if daily else LINE
            o.append(f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="34" rx="8" fill="#0e1420" stroke="{bd}" stroke-width="1.25"/>')
            o.append(f'<text x="{x+cw/2:.0f}" y="{y+22}" font-size="13" fill="{INK}" text-anchor="middle">{esc(name)}</text>')
            x+=cw+10
        y+=step
    o.append('</svg>'); W("stack.svg","\n".join(o))

def header(slug,label,meta):
    w,h=940,56
    o=[head(w,h,label),'<defs>'+bg("h"+slug)+'</defs>',frame(w,h,"h"+slug)]
    o.append(f'<text x="34" y="35" font-size="13.5" letter-spacing="3" fill="{MUT}"><tspan fill="{AMBER}">//</tspan> {esc(label)}</text>')
    o.append(f'<text x="{w-34}" y="35" font-size="11.5" letter-spacing="2" fill="{MUT}" text-anchor="end">{esc(meta)}</text>')
    o.append('</svg>'); A(f"hdr_{slug}.svg","\n".join(o))

def card(slug,name,tag,tagline,accent):
    w,h=470,150
    o=[head(w,h,f"{name} — {tagline}"),f'<rect width="{w}" height="{h}" rx="14" fill="{PANEL}"/>',
       f'<rect width="{w}" height="{h}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.25"/>',
       f'<rect x="0" y="10" width="5" height="{h-20}" rx="2.5" fill="{accent}"/>',
       f'<text x="28" y="50" font-size="18" font-weight="700" fill="{INK}">{esc(name)}</text>']
    cw=len(tag)*8.2+24
    o.append(f'<rect x="{w-28-cw:.0f}" y="29" width="{cw:.0f}" height="26" rx="8" fill="#0e1420" stroke="{LINE}"/>')
    o.append(f'<text x="{w-28-cw/2:.0f}" y="46" font-size="11.5" fill="{MUT}" text-anchor="middle">{esc(tag)}</text>')
    o.append(f'<text x="28" y="88" font-size="13.5" font-family="{SERIF}" font-style="italic" fill="#aeb7c9">{esc(tagline)}</text>')
    o.append(f'<text x="28" y="124" font-size="11.5" letter-spacing="1.5" fill="{accent}">open &#8594;</text>')
    o.append('</svg>'); A(f"card_{slug}.svg","\n".join(o))

def linkbtn(slug,label,sub,accent):
    w,h=313,80   # 940/3 so 3-col link buttons render at the same scale as 2-col cards
    o=[head(w,h,f"{label} — {sub}"),f'<rect width="{w}" height="{h}" rx="12" fill="{PANEL}"/>',
       f'<rect width="{w}" height="{h}" rx="12" fill="none" stroke="{LINE}" stroke-width="1.25"/>',
       f'<rect x="0" y="10" width="5" height="{h-20}" rx="2.5" fill="{accent}"/>',
       f'<text x="24" y="34" font-size="11.5" letter-spacing="2.5" fill="{MUT}">{esc(label)}</text>',
       f'<text x="24" y="58" font-size="14" fill="{INK}">{esc(sub)}</text>',
       f'<text x="{w-20}" y="32" font-size="14" fill="{accent}" text-anchor="end">&#8599;</text>','</svg>']
    A(f"link_{slug}.svg","\n".join(o))

experience(); stack()
header("built","THINGS WITH A FACE ON THEM","self-contained · no dependencies")
header("elsewhere","ELSEWHERE","the rest of me")
CARDS=[("minutes","Minutes","macOS · Swift","meetings → notes, on-device",AMBER),
 ("bulwark","Bulwark","Chrome · MV3","ad, popup & redirect blocker",AMBER),
 ("clipboardmanager","ClipboardManager","macOS · Swift","clipboard history, ⌘⌃V",AMBER),
 ("blobtodo","BlobTodo","macOS · SwiftUI","a floating todo widget",AMBER),
 ("meetingreminder","MeetingReminder","macOS · Swift","a banner before every meeting",AMBER),
 ("tabdeck","TabDeck","Chrome · MV3","manual tab grouping that stays",AMBER),
 ("solarsystem","Orrery","WebGL2","an explorable Solar System",OK),
 ("humananatomy","Corpus","WebGL2","a dissectable human body",OK),
 ("cpuanatomy","Silicon","WebGL2","an anatomy of a CPU",OK),
 ("winsim","WinSim","vanilla JS","Windows XP & Vista in a tab",OK),
 ("voidgraze","VoidGraze","Canvas","a bullet-hell scored on uptime",OK),
 ("passportsheet","Passport Sheet","Canvas","4×6 passport-photo print tool",OK)]
for a in CARDS: card(*a)
linkbtn("portfolio","PORTFOLIO","souravkundu.dev",AMBER)
linkbtn("labs","LABS","souravkundu.dev/labs",OK)
linkbtn("linkedin","LINKEDIN","in/souravkundu1998",BLUE)
print("done")
