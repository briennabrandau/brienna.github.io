"""Builds the site's index.html.

Run from anywhere:  python3 source/build.py
Edit the text in source/content/*.html or in this file, then rebuild.
"""
import re, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load(name):
    with open(os.path.join(HERE, 'content', name + '.html')) as f:
        return f.read()

experience = load('experience')   # Experience page: the job entries
education = load('education')     # Studies page: degree card
focus = load('focus')             # Studies page: "Where I'm headed" cards
life = load('life')               # Off the clock page: hobby cards

# ---------- soft sea glass ----------
def star_path(cx, cy, R, r, n=5, rot=-90):
    pts = []
    for i in range(n*2):
        a = math.radians(rot + i*180/n)
        rad = R if i % 2 == 0 else r
        pts.append(f'{cx+rad*math.cos(a):.1f},{cy+rad*math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + ' Z'


def round_poly(pts, r):
    n = len(pts); out = []
    for i in range(n):
        p0, p1, p2 = pts[i-1], pts[i], pts[(i+1) % n]
        def toward(a, b, d):
            dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy); d = min(d, L/2.2)
            return (a[0]+dx/L*d, a[1]+dy/L*d)
        a = toward(p1, p0, r); b = toward(p1, p2, r)
        out.append(f"{'M' if i == 0 else 'L'}{a[0]:.1f},{a[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {b[0]:.1f},{b[1]:.1f}")
    return ' '.join(out) + ' Z'
def star_pts(cx, cy, R, r, n=5, rot=-90):
    return [(cx+(R if i%2==0 else r)*math.cos(math.radians(rot+i*180/n)), cy+(R if i%2==0 else r)*math.sin(math.radians(rot+i*180/n))) for i in range(n*2)]

GLASS = {
  'experience': dict(light='#fbfcfa', base='#e6ece8', deep='#c9d6d0', shadow='#a9bab3', sw=0,
                     d='M118,206 C140,186 188,190 206,214 C224,238 214,278 188,292 C158,306 114,298 99,272 C85,248 96,222 118,206 Z'),
  'studies':    dict(light='#f4dfbb', base='#d8b07a', deep='#b48650', shadow='#c39a66', sw=0,
                     d=round_poly([(100,224),(150,192),(212,204),(214,264),(174,298),(106,286)], 16)),
  'life':       dict(light='#dcefe0', base='#a9cfb2', deep='#7fa98a', shadow='#8db79a', sw=0,
                     d=round_poly(star_pts(154, 248, 70, 34), 12)),
}
def piece(key, uid, transform=''):
    g = GLASS[key]
    stroke = f' stroke="url(#gf-{uid})" stroke-width="{g["sw"]}" stroke-linejoin="round"' if g['sw'] else ''
    clipstroke = f' stroke="#000" stroke-width="{g["sw"]}" stroke-linejoin="round"' if g['sw'] else ''
    return f'''
      <defs>
        <radialGradient id="gf-{uid}" cx="38%" cy="30%" r="80%">
          <stop offset="0" stop-color="{g['light']}" stop-opacity=".95"/><stop offset=".55" stop-color="{g['base']}" stop-opacity=".9"/><stop offset="1" stop-color="{g['deep']}" stop-opacity=".92"/>
        </radialGradient>
        <clipPath id="gc-{uid}"><path d="{g['d']}"{clipstroke}/></clipPath>
      </defs>
      <g transform="{transform}">
        <path d="{g['d']}" transform="translate(16 18)" fill="{g['shadow']}" opacity=".38" filter="url(#blur10)"{clipstroke.replace('#000', g['shadow'])}/>
        <path d="{g['d']}" transform="translate(9 10)" fill="{g['light']}" opacity=".45" filter="url(#blur6)"/>
        <g filter="url(#blur05)">
          <path d="{g['d']}" fill="url(#gf-{uid})"{stroke}/>
          <g clip-path="url(#gc-{uid})">
            <rect x="0" y="100" width="300" height="300" filter="url(#frost)" opacity=".5"/>
            <path d="{g['d']}" fill="none" stroke="#ffffff" stroke-width="{10 + g['sw']}" stroke-linejoin="round" opacity=".5" filter="url(#blur4)"/>
            <ellipse cx="130" cy="222" rx="34" ry="12" fill="#fff" opacity=".35" filter="url(#blur6)" transform="rotate(-20 130 222)"/>
          </g>
        </g>
      </g>'''

def shore_bg(uid, water=0.26, extra=''):
    wy = 400*water
    return f'''
      <defs>
        <linearGradient id="sand-{uid}" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#e9dfcf"/><stop offset=".5" stop-color="#efe7da"/><stop offset="1" stop-color="#e6dac6"/></linearGradient>
        <linearGradient id="sea-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9d3cf"/><stop offset=".7" stop-color="#d7e5e1"/><stop offset="1" stop-color="#e8efea" stop-opacity="0"/></linearGradient>
      </defs>
      <rect width="300" height="420" fill="url(#sand-{uid})"/>
      <path d="M0,{wy+30} C60,{wy+18} 110,{wy+44} 170,{wy+30} S260,{wy+16} 300,{wy+28} V{wy+60} H0 Z" fill="#ddd0bb" opacity=".55" filter="url(#blur10)"/>
      <path d="M0,0 H300 V{wy} C250,{wy+16} 200,{wy-6} 150,{wy+10} S50,{wy+2} 0,{wy+14} Z" fill="url(#sea-{uid})"/>
      <path d="M0,{wy+14} C50,{wy+2} 100,{wy+22} 150,{wy+10} S250,{wy-4} 300,{wy+6}" fill="none" stroke="#fff" stroke-width="5" opacity=".85" filter="url(#blur2)"/>
      <path d="M0,{wy+26} C60,{wy+16} 120,{wy+34} 180,{wy+22} S270,{wy+14} 300,{wy+20}" fill="none" stroke="#fff" stroke-width="2" opacity=".5" stroke-dasharray="1 7" stroke-linecap="round" filter="url(#blur05)"/>
      {extra}
      <g fill="#cbbba2" opacity=".55"><circle cx="40" cy="330" r="1.3"/><circle cx="250" cy="360" r="1.1"/><circle cx="220" cy="180" r="1"/><circle cx="70" cy="200" r="1.2"/><circle cx="190" cy="380" r="1.4"/><circle cx="268" cy="250" r="1"/></g>
      <rect width="300" height="420" filter="url(#grain)" opacity=".5"/>'''

def arch(key, uid, cls=''):
    return f'''<svg class="arch-art {cls}" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{shore_bg(uid)}{piece(key, uid, 'translate(0 10)')}
    </svg>'''

about_arch = f'''<svg class="arch-art" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{shore_bg('about', 0.42)}
      {piece('experience', 'a1', 'translate(10 70) scale(.55)')}
      {piece('studies', 'a2', 'translate(150 140) scale(.5)')}
      {piece('life', 'a3', 'translate(40 230) scale(.45)')}
    </svg>'''


def crystal_arch(uid):
    rings = ''.join(f'<ellipse class="ring" cx="150" cy="262" rx="{60+i*34}" ry="{22+i*13}" style="animation-delay:{-i*1.6:.1f}s"/>' for i in range(6))
    sparks = ''.join(f'<path d="M{x},{y-r} Q{x+1.2},{y-1.2} {x+r},{y} Q{x+1.2},{y+1.2} {x},{y+r} Q{x-1.2},{y+1.2} {x-r},{y} Q{x-1.2},{y-1.2} {x},{y-r} Z" class="spark" style="animation-delay:{d}s"/>'
                     for x, y, r, d in [(70,120,9,0),(232,96,6,-1.2),(214,190,7,-2.4),(88,330,5,-.8),(246,340,8,-3.1),(150,70,5,-1.9)])
    return f"""<svg class="arch-art crystal" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <radialGradient id="pearl-{uid}" cx="50%" cy="58%" r="75%"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f4f3f8"/><stop offset="1" stop-color="#e7e5ef"/></radialGradient>
      </defs>
      <rect width="300" height="420" fill="url(#pearl-{uid})"/>
      <g filter="url(#blur10)" opacity=".35">
        <ellipse cx="60" cy="90" rx="90" ry="70" fill="#e4ddf6"/><ellipse cx="250" cy="150" rx="80" ry="90" fill="#d9eff1"/>
        <ellipse cx="80" cy="360" rx="100" ry="60" fill="#f6e2ea"/><ellipse cx="240" cy="380" rx="80" ry="50" fill="#f1ead8"/>
      </g>
      <g class="rings" fill="none" stroke="#b9b0dc" stroke-width="1">{rings}</g>
      {piece('experience', uid, 'translate(0 24)')}
      <g fill="#ffffff" filter="url(#blur05)">{sparks}</g>
      <rect width="300" height="420" filter="url(#grain)" opacity=".25"/>
    </svg>"""


def sunset_arch(uid):
    steps = ''.join(f'<g transform="translate({x} {y}) rotate({r})"><ellipse cx="-4" cy="0" rx="3.2" ry="5.5"/><ellipse cx="4" cy="-9" rx="3.2" ry="5.5"/></g>'
                    for x, y, r in [(70,410,-30),(92,380,-28),(112,352,-26),(132,326,-24),(150,302,-22)])
    return f"""<svg class="arch-art" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="sky-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b7a9c8"/><stop offset=".45" stop-color="#e6b6c3"/><stop offset=".8" stop-color="#f5c7a6"/><stop offset="1" stop-color="#ffe0ae"/></linearGradient>
        <linearGradient id="ocean-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7aa7ab"/><stop offset="1" stop-color="#5f9a9b"/></linearGradient>
        <linearGradient id="wet-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3c2bd"/><stop offset=".5" stop-color="#d6b39f"/><stop offset="1" stop-color="#c9a588"/></linearGradient>
        <radialGradient id="glow-{uid}" cx="190" cy="196" r="150" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff1c8" stop-opacity=".95"/><stop offset=".4" stop-color="#ffd7a6" stop-opacity=".5"/><stop offset="1" stop-color="#ffd7a6" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="300" height="200" fill="url(#sky-{uid})"/>
      <circle cx="190" cy="196" r="150" fill="url(#glow-{uid})"/>
      <g filter="url(#blur6)">
        <ellipse cx="80" cy="60" rx="110" ry="18" fill="#efd0d8" opacity=".8"/><ellipse cx="230" cy="40" rx="90" ry="14" fill="#d8c3da" opacity=".8"/>
        <ellipse cx="200" cy="110" rx="120" ry="12" fill="#f6d2cf" opacity=".85"/><ellipse cx="60" cy="140" rx="90" ry="10" fill="#f9dcc6" opacity=".8"/>
        <ellipse cx="250" cy="160" rx="70" ry="7" fill="#fff0d8" opacity=".9"/>
      </g>
      <path d="M0,96 C18,94 30,104 38,118 C46,132 44,150 54,166 C60,178 74,188 86,198 L0,206 Z" fill="#7b6463"/>
      <path d="M0,120 C16,122 26,136 34,152 C40,166 50,182 70,198 L0,204 Z" fill="#665252" opacity=".7"/>
      <rect y="196" width="300" height="70" fill="url(#ocean-{uid})"/>
      <g fill="#f6cdbd" opacity=".55"><rect x="150" y="204" width="90" height="2" rx="1"/><rect x="164" y="214" width="60" height="2" rx="1"/><rect x="176" y="224" width="40" height="2" rx="1"/></g>
      <path d="M0,246 C40,232 70,226 110,232 C150,238 190,226 230,224 C260,222 284,230 300,236 V270 H0 Z" fill="#4f8b8d" opacity=".8"/>
      <path d="M0,250 C40,236 72,232 112,238 C152,244 192,232 232,230 C262,228 286,236 300,240" fill="none" stroke="#ffffff" stroke-width="9" opacity=".9" filter="url(#blur2)"/>
      <path d="M0,262 C50,254 100,266 150,258 S250,250 300,258 V420 H0 Z" fill="url(#wet-{uid})"/>
      <path d="M0,262 C50,254 100,266 150,258 S250,250 300,258 V286 C240,280 180,292 120,286 S30,282 0,290 Z" fill="#ffffff" opacity=".55" filter="url(#blur4)"/>
      <path d="M0,290 C30,282 80,288 120,286 S240,280 300,286" fill="none" stroke="#ffffff" stroke-width="2.5" opacity=".9" filter="url(#blur05)"/>
      <g fill="#f3c9bd" opacity=".45"><rect x="150" y="300" width="80" height="2" rx="1"/><rect x="170" y="312" width="50" height="2" rx="1"/></g>
      <g fill="#b38f75" opacity=".5">{steps}</g>
      {piece('life', uid, 'translate(110 230) scale(.42)')}
      <rect width="300" height="420" filter="url(#grain)" opacity=".35"/>
    </svg>"""


def gg_arch(uid):
    def tower(x):
        l, r = x - 9, x + 4
        out = [f'<rect x="{l}" y="66" width="5" height="160"/>', f'<rect x="{r}" y="66" width="5" height="160"/>',
               f'<rect x="{l-1}" y="62" width="7" height="5"/>', f'<rect x="{r-1}" y="62" width="7" height="5"/>']
        out += [f'<rect x="{l}" y="{y}" width="{r - l + 5}" height="{h}"/>' for y, h in [(76, 6), (110, 5), (140, 4), (196, 5)]]
        return ''.join(out)
    hangers = ''.join(f'<line x1="{x}" y1="{y:.1f}" x2="{x}" y2="175"/>' for x, y in
                      [(x, 74 + (200 - 74) * 2 * ((x - 90) / 160) * (1 - (x - 90) / 160)) for x in range(102, 246, 9)])
    return f"""<svg class="arch-art" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="gsky-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9cde0"/><stop offset=".5" stop-color="#d9e2d6"/><stop offset=".82" stop-color="#f6dca2"/><stop offset="1" stop-color="#fbe9bf"/></linearGradient>
        <linearGradient id="gbay-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fbccb"/><stop offset="1" stop-color="#78aab9"/></linearGradient>
        <linearGradient id="gsand-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ead8bf"/><stop offset="1" stop-color="#e2cba9"/></linearGradient>
        <radialGradient id="gsun-{uid}" cx="200" cy="205" r="140" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff3d2" stop-opacity=".95"/><stop offset="1" stop-color="#ffe2b4" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="300" height="215" fill="url(#gsky-{uid})"/>
      <circle cx="200" cy="205" r="140" fill="url(#gsun-{uid})"/>
      <circle cx="200" cy="200" r="20" fill="#fff4da" opacity=".9" filter="url(#blur2)"/>
      <g filter="url(#blur6)" opacity=".8"><ellipse cx="70" cy="70" rx="100" ry="12" fill="#ffffff"/><ellipse cx="230" cy="120" rx="90" ry="9" fill="#fff6e2"/></g>
      <path d="M0,196 C30,180 60,178 90,190 C110,198 130,204 150,212 L0,214 Z" fill="#a7b7a6" opacity=".8"/>
      <path d="M220,212 C240,196 270,186 300,188 V214 Z" fill="#98aa99" opacity=".8"/>
      <g class="ggb">
        <g stroke="#cf8a72" stroke-width="1" opacity=".8">{hangers}</g>
        <path d="M0,150 Q50,124 90,72 Q170,200 250,72 Q280,104 300,112" fill="none" stroke="#c97e66" stroke-width="2.4"/>
        <rect x="0" y="174" width="300" height="5" fill="#c97e66"/>
        <rect x="0" y="179" width="300" height="3" fill="#b06a55" opacity=".8"/>
        <g fill="#cd8168">{tower(90)}{tower(250)}</g>
      </g>
      <rect y="212" width="300" height="70" fill="url(#gbay-{uid})"/>
      <g fill="#fff1d6" opacity=".7"><rect x="170" y="220" width="60" height="2" rx="1"/><rect x="182" y="230" width="36" height="2" rx="1"/><rect x="190" y="240" width="20" height="2" rx="1"/></g>
      <rect x="0" y="196" width="300" height="30" fill="#ffffff" opacity=".45" filter="url(#blur6)"/>
      <path d="M0,276 C60,266 120,282 180,272 S260,264 300,270 V420 H0 Z" fill="url(#gsand-{uid})"/>
      <path d="M0,276 C60,266 120,282 180,272 S260,264 300,270" fill="none" stroke="#ffffff" stroke-width="4" opacity=".85" filter="url(#blur2)"/>
      {piece('studies', uid, 'translate(70 228) scale(.5)')}
      <rect width="300" height="420" filter="url(#grain)" opacity=".35"/>
    </svg>"""


def morning_arch(uid):
    return f"""<svg class="arch-art" viewBox="0 0 300 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="msky-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9d8ea"/><stop offset=".7" stop-color="#d6eef0"/><stop offset="1" stop-color="#eef7f2"/></linearGradient>
        <linearGradient id="msea-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fb3c0"/><stop offset=".55" stop-color="#6fcac8"/><stop offset="1" stop-color="#9fe0d6"/></linearGradient>
        <linearGradient id="mshallow-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9ece2" stop-opacity=".95"/><stop offset="1" stop-color="#d9f4ec" stop-opacity=".5"/></linearGradient>
        <linearGradient id="msand-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e8d4"/><stop offset="1" stop-color="#ead9bd"/></linearGradient>
      </defs>
      <rect width="300" height="200" fill="url(#msky-{uid})"/>
      <circle cx="220" cy="62" r="20" fill="#fffdf4"/>
      <circle cx="220" cy="62" r="60" fill="#fffbe8" opacity=".55" filter="url(#blur10)"/>
      <g fill="#ffffff" filter="url(#blur2)">
        <ellipse cx="70" cy="90" rx="46" ry="12" opacity=".95"/><ellipse cx="98" cy="82" rx="28" ry="14" opacity=".95"/><ellipse cx="52" cy="84" rx="22" ry="10" opacity=".9"/>
        <ellipse cx="236" cy="130" rx="40" ry="9" opacity=".85"/><ellipse cx="256" cy="124" rx="22" ry="10" opacity=".85"/>
      </g>
      <rect y="196" width="300" height="70" fill="url(#msea-{uid})"/>
      <g fill="#ffffff" opacity=".45"><rect x="30" y="206" width="50" height="2" rx="1"/><rect x="150" y="214" width="70" height="2" rx="1"/><rect x="80" y="226" width="60" height="2" rx="1"/><rect x="210" y="236" width="50" height="2" rx="1"/></g>
      <path d="M0,262 C60,250 120,268 180,256 S260,248 300,254 V420 H0 Z" fill="url(#msand-{uid})"/>
      <path d="M0,258 C60,246 120,264 180,252 S260,244 300,250 V300 C240,292 170,306 110,298 S30,294 0,304 Z" fill="url(#mshallow-{uid})"/>
      <g fill="none" stroke="#ffffff" stroke-width="1.4" opacity=".6" filter="url(#blur05)">
        <path d="M20,276 q14,-6 28,0 t28,0"/><path d="M150,284 q14,-6 28,0 t28,0"/><path d="M90,292 q12,-5 24,0 t24,0"/><path d="M220,272 q12,-5 24,0"/>
      </g>
      <path d="M0,304 C30,294 110,298 110,298 S240,292 300,300" fill="none" stroke="#ffffff" stroke-width="3" opacity=".9" filter="url(#blur05)"/>
      {piece('experience', uid, 'translate(62 222) scale(.6)')}
      <rect width="300" height="420" filter="url(#grain)" opacity=".3"/>
    </svg>"""


def temple(uid):
    def a(o):
        r = 150 + o
        return f'M{-o},{420+o} V150 A{r},{r} 0 0 1 {300+o},150 V{420+o} Z'
    flutes = ''.join(f'<line x1="{x}" y1="168" x2="{x}" y2="414"/><line x1="{300-x}" y1="168" x2="{300-x}" y2="414"/>' for x in (-13, -9.5, -6))
    return f"""<svg class="temple" viewBox="-21 -23 342 474" aria-hidden="true">
        <defs><linearGradient id="mb-{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf9f5"/><stop offset=".5" stop-color="#f1ece3"/><stop offset="1" stop-color="#e9e2d6"/></linearGradient></defs>
        <path d="{a(16)} {a(4)}" fill="url(#mb-{uid})" fill-rule="evenodd" stroke="#dacfbd" stroke-width=".8"/>
        <path d="{a(7)}" fill="none" stroke="#c9ab72" stroke-width=".9"/>
        <path d="{a(13.5)}" fill="none" stroke="#c9ab72" stroke-width=".5" opacity=".7"/>
        <g stroke="#ddd3c3" stroke-width=".7">{flutes}</g>
        <g fill="url(#mb-{uid})" stroke="#c9ab72" stroke-width=".8">
          <path d="M141,-20 L159,-20 L156,-2 L144,-2 Z"/>
          <rect x="-21" y="146" width="24" height="7" rx="1"/><rect x="297" y="146" width="24" height="7" rx="1"/>
          <rect x="-19" y="153" width="20" height="5"/><rect x="299" y="153" width="20" height="5"/>
          <rect x="-23" y="418" width="346" height="8" rx="1"/><rect x="-27" y="426" width="354" height="10" rx="1"/>
        </g>
        <g fill="none" stroke="#c9ab72" stroke-width=".8"><circle cx="-17" cy="160" r="2.4"/><circle cx="-3" cy="160" r="2.4"/><circle cx="303" cy="160" r="2.4"/><circle cx="317" cy="160" r="2.4"/></g>
      </svg>"""

INFO = {
  'experience': ('Experience', "where I've worked"),
  'studies': ('Studies', "what I'm learning"),
  'life': ('Off the clock', 'life by the water'),
}

def view(key, intro, body, deco='', extra=''):
    title, cap = INFO[key]
    links = ''.join(f'<a href="#{k}"{" aria-current=\"page\"" if k == key else ""}>{INFO[k][0]}</a>' for k in INFO)
    return f'''
<section class="view gutter" id="view-{key}" hidden>{deco}
  <div class="wrap">
    <nav class="topbar" aria-label="Pages">
      <a class="back" href="#">← the shore</a>
      <div class="toplinks">{links}</div>
    </nav>
    <header class="view-head">
      <div class="arch small">{morning_arch('v-' + key) if key == 'experience' else sunset_arch('v-' + key) if key == 'life' else gg_arch('v-' + key)}</div>
      <div class="view-title">
        <span class="label">{cap}</span>
        <h2>{title}</h2>
        <p class="view-intro">{intro}</p>{extra}
      </div>
    </header>
    <div class="view-body">
{body}
    </div>
  </div>
</section>'''

views = (
  view('experience', "A little bit of everything, and all of it has shaped who I am.",
       '<div class="log">' + experience.split('<div class="log">', 1)[1],
       deco='\n  <div class="halo" aria-hidden="true"></div>') +
  view('studies', "Civil engineering and philosophy at UC Berkeley: how to build things that last, and who they're for.",
       education + '''
      <h3 class="sub">Capstone project</h3>
      <article class="project">
        <div class="edu-head"><span class="label">Capstone · In progress</span><span class="label">Pacifica, CA</span></div>
        <h4>Pacifica Coastal Erosion Decision Tool</h4>
        <p>Pacifica is losing its coastline fast, and the city has to choose between building a seawall, managed retreat, or doing nothing. I'm building a tool that shows when a seawall stops making financial sense compared with retreat, and turns that answer into a summary a city could use in a grant application.</p>
        <p>It adds up the cost of each option year by year through 2100 under low and high sea-level rise, finds the year when acting becomes cheaper than waiting, and checks the results against the city's own 2018 study. An early check already lines up: the erosion rates I measured at Esplanade Avenue, up to about 9 feet a year, match the city's report of 90 feet of bluff loss in a decade.</p>
        <dl class="facts">
          <div><dt>Focus</dt><dd>West Sharp Park, from Beach Blvd to Esplanade Ave</dd></div>
          <div><dt>Data</dt><dd>USGS shoreline and sea-level projections, city cost studies</dd></div>
          <div><dt>Tools</dt><dd>Python, Streamlit, QGIS, Google Sheets</dd></div>
        </dl>
      </article>
      <h3 class="sub">Where I\'m headed</h3>
''' + focus) +
  view('life', "When I'm not in class or at work, I'm usually somewhere near the water.", life)
)

cards = ''.join(f'''
        <a class="card-arch" href="#{k}">
          <div class="frame"><div class="arch">{arch(k, 'h-' + k)}</div>{temple('t-' + k)}</div>
          <span class="card-title">{INFO[k][0]}</span>
          <span class="card-cap">{INFO[k][1]}</span>
        </a>''' for k in INFO)

GRAIN = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .38 0 0 0 0 .3 0 0 0 .22 0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E\")"

html = f'''<title>Brienna Brandau</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Brienna Brandau: civil engineering and philosophy student at UC Berkeley.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap">
<style>
/* Layout: an airy editorial page on warm sand. Three arch-framed stills of sea glass lead to their own pages; about and contact follow quietly below. One soft light look in every theme. */
:root {{
  --paper: #f6f1e9;
  --sand: #ece3d5;
  --ink: #3d3a35;
  --soft: #8a8178;
  --hair: #ddd2c2;
  --mist: #c9dad5;
  --sea: #7fa7a0;
  --clay: #b98a62;
  --display: "Cormorant Garamond", "Cormorant", Garamond, Georgia, serif;
  --body: "Jost", "Futura", "Helvetica Neue", Arial, sans-serif;
  color-scheme: light;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: var(--body); font-weight: 300; font-size: 1.05rem; line-height: 1.75; }}
body::after {{ content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 40; background-image: {GRAIN}; opacity: .55; }}
a {{ color: inherit; }}
a:focus-visible {{ outline: 1px solid var(--ink); outline-offset: 6px; }}
p {{ margin: 0; }}
strong {{ font-weight: 500; }}
.gutter {{ padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }}
.wrap {{ max-width: 1040px; margin: 0 auto; }}
.label {{ font-family: var(--body); font-weight: 400; font-size: .68rem; letter-spacing: .28em; text-transform: uppercase; color: var(--soft); }}
h1, h2 {{ font-family: var(--display); font-weight: 300; margin: 0; letter-spacing: -.01em; }}
h2 {{ font-size: clamp(2.4rem, 6vw, 3.6rem); line-height: 1; font-style: italic; }}
h3 {{ margin: 0; }}

/* top line */
.topbar {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding-block: 26px; flex-wrap: wrap; }}
.topbar .mark {{ font-family: var(--display); font-style: italic; font-size: 1.25rem; text-decoration: none; }}
.toplinks {{ display: flex; gap: 24px; flex-wrap: wrap; }}
.toplinks a, .back {{ font-size: .7rem; letter-spacing: .24em; text-transform: uppercase; text-decoration: none; color: var(--soft); padding-block: 4px; border-bottom: 1px solid transparent; transition: color .3s, border-color .3s; }}
.toplinks a:hover, .back:hover, .toplinks a[aria-current="page"] {{ color: var(--ink); border-color: var(--ink); }}

/* landing */
.intro {{ text-align: center; display: grid; justify-items: center; gap: 18px; padding-block: 170px 56px; }}
#home {{ position: relative; isolation: isolate; }}
#mosaic {{ position: absolute; left: 0; top: 0; width: 100%; height: 300px; z-index: -1; display: block; pointer-events: none; }}
#home .topbar .mark, #home .toplinks a {{ background: rgba(246, 241, 233, .82); color: var(--ink); padding: 6px 14px; border-radius: 999px; -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); border-bottom: 0; }}
#home .toplinks {{ gap: 8px; }}
#home .toplinks a:hover {{ background: rgba(246, 241, 233, .97); }}
.wave-rule {{ width: 120px; height: 14px; color: var(--sea); }}
h1 {{ font-size: clamp(3.4rem, 11vw, 7.5rem); line-height: .9; }}
h1 em {{ font-style: italic; }}
.lede {{ font-family: var(--display); font-size: clamp(1.25rem, 2.6vw, 1.55rem); line-height: 1.45; max-width: 30em; color: #5a554e; text-wrap: balance; }}
.cards {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(14px, 3.5vw, 44px); }}
.card-arch {{ display: grid; justify-items: center; gap: 6px; text-decoration: none; text-align: center; }}
.arch {{ width: 100%; aspect-ratio: 3 / 4.2; border-radius: 999px 999px 6px 6px; overflow: hidden; background: var(--sand); max-width: 100%; }}
.arch-art {{ display: block; width: 100%; height: 100%; }}
.card-arch .arch-art {{ transition: transform 1.2s cubic-bezier(.2,.7,.2,1); }}
@media (prefers-reduced-motion: no-preference) {{ .card-arch:hover .arch-art, .card-arch:focus-visible .arch-art {{ transform: scale(1.05); }} }}
.card-title {{ font-family: var(--display); font-style: italic; font-size: clamp(1.35rem, 3vw, 1.9rem); line-height: 1.1; margin-top: 14px; }}
.card-cap {{ font-size: .68rem; letter-spacing: .26em; text-transform: uppercase; color: var(--soft); }}
.card-arch:hover .card-title {{ text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 6px; }}
.note {{ text-align: center; font-family: var(--display); font-style: italic; color: var(--soft); font-size: 1.15rem; padding-block: 36px 0; }}

/* about */
.about {{ display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(28px, 6vw, 80px); align-items: center; padding-block: 120px 40px; scroll-margin-top: 20px; }}
.about .arch {{ max-width: 420px; justify-self: center; }}
.about-text {{ display: grid; gap: 20px; min-width: 0; }}
.about-text p {{ max-width: 60ch; }}
.quote {{ padding-block: 80px 40px; text-align: center; display: grid; justify-items: center; gap: 22px; }}
.quote blockquote {{ margin: 0; font-family: var(--display); font-style: italic; font-weight: 300; font-size: clamp(1.5rem, 3.6vw, 2.25rem); line-height: 1.35; max-width: 30em; text-wrap: balance; }}

/* contact */
.contact {{ text-align: center; display: grid; justify-items: center; gap: 18px; padding-block: 90px 110px; border-top: 1px solid var(--hair); margin-top: 60px; scroll-margin-top: 20px; }}
.contact p.big {{ font-family: var(--display); font-size: clamp(1.25rem, 2.8vw, 1.6rem); line-height: 1.45; max-width: 28em; color: #5a554e; }}
.email {{ font-family: var(--display); font-size: clamp(1.6rem, 4.5vw, 2.4rem); font-style: italic; user-select: all; word-break: break-all; }}
.links {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 28px; }}
.textbtn {{ font: 400 .7rem var(--body); letter-spacing: .24em; text-transform: uppercase; color: var(--ink); background: none; border: 0; border-bottom: 1px solid var(--ink); padding: 4px 0; cursor: pointer; text-decoration: none; }}
.textbtn:hover {{ color: var(--clay); border-color: var(--clay); }}
footer {{ display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; padding-block: 0 36px; }}

/* subpages */
.view-head {{ display: grid; grid-template-columns: minmax(0, 260px) minmax(0, 1fr); gap: clamp(24px, 6vw, 72px); align-items: end; padding-block: 30px 40px; border-bottom: 1px solid var(--hair); }}
.view-title {{ display: grid; gap: 12px; padding-bottom: 12px; }}
.view-title h2 {{ font-size: clamp(3rem, 8vw, 5.2rem); }}
.view-intro {{ font-family: var(--display); font-size: clamp(1.2rem, 2.4vw, 1.45rem); line-height: 1.45; color: #5a554e; max-width: 30em; }}
.view-body {{ max-width: 780px; margin-left: auto; padding-block: 24px 110px; display: grid; gap: 24px; }}
h2:focus {{ outline: none; }}
.log {{ display: grid; }}
.entry {{ display: grid; grid-template-columns: 8.5rem minmax(0, 1fr); gap: 24px; padding-block: 30px; border-bottom: 1px solid var(--hair); }}
.entry time {{ font-size: .68rem; letter-spacing: .2em; text-transform: uppercase; color: var(--soft); padding-top: 6px; }}
.entry .org {{ font-size: .68rem; letter-spacing: .24em; text-transform: uppercase; color: var(--sea); }}
.entry h3 {{ font-family: var(--display); font-style: italic; font-weight: 400; font-size: 1.75rem; line-height: 1.15; margin: 6px 0 10px; }}
.story {{ max-width: 56ch; }}
.edu {{ display: grid; gap: 14px; padding-block: 30px; border-bottom: 1px solid var(--hair); }}
.edu-head {{ display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px 16px; }}
.edu .label {{ font-size: .68rem; }}
.degrees {{ font-family: var(--display); font-style: italic; font-size: 1.9rem; line-height: 1.2; }}
h3.sub {{ font-family: var(--display); font-weight: 300; font-style: italic; font-size: 2.2rem; margin-top: 40px; }}
.focus {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; }}
.focus .card {{ border-top: 1px solid var(--ink); padding-top: 16px; display: grid; gap: 8px; align-content: start; }}
.focus .card h3 {{ font-family: var(--display); font-weight: 400; font-style: italic; font-size: 1.45rem; line-height: 1.15; }}
.focus .card p {{ color: #6b655d; font-size: .98rem; }}
.shore {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 40px; }}
.shore div {{ padding-block: 22px; border-bottom: 1px solid var(--hair); display: grid; gap: 4px; }}
.shore h3 {{ font-family: var(--display); font-weight: 400; font-style: italic; font-size: 1.6rem; line-height: 1.15; }}
.shore p {{ color: #6b655d; }}

@media (prefers-reduced-motion: no-preference) {{
  .view:not([hidden]) .view-head, .view:not([hidden]) .view-body {{ animation: fade .8s ease both; }}
  .view:not([hidden]) .view-body {{ animation-delay: .1s; }}
}}

/* experience: bright midday */
#view-experience {{ position: relative; isolation: isolate; min-height: 100vh; background: linear-gradient(180deg, #dcf0ee 0%, #e9f5f0 30%, #f3f4ec 65%, #f6f1e9 100%); }}
.halo {{ position: absolute; inset: 0 0 auto 0; height: 700px; z-index: -1; pointer-events: none;
  background: radial-gradient(ellipse 50% 55% at 80% 0%, rgba(255, 253, 240, .9) 0%, rgba(255, 253, 240, 0) 70%); }}
#view-experience .view-head {{ border-bottom: 1px solid #cfe5e1; }}
#view-experience .arch {{ box-shadow: 0 24px 50px -30px rgba(40, 120, 120, .35); }}
#view-experience .label, #view-experience .entry time {{ color: #5f8f8c; }}
#view-experience .log {{ gap: 14px; }}
#view-experience .entry {{ background: rgba(255, 255, 255, .8); border: 1px solid rgba(255, 255, 255, .95); border-radius: 20px; padding: 28px 32px; box-shadow: 0 14px 40px -32px rgba(40, 110, 110, .4); }}
#view-experience .entry:last-child {{ border-bottom: 1px solid rgba(255, 255, 255, .95); }}
#view-experience .entry .story {{ color: #3a3d3c; }}
#view-experience .entry .org {{ color: #2f9294; }}
@media (max-width: 720px) {{ #view-experience .entry {{ padding: 22px 20px; }} }}

/* off the clock: soft sunset */
#view-life {{ min-height: 100vh; background: linear-gradient(180deg, #efe0e8 0%, #f6e3d9 30%, #f7ece2 60%, #f6f1e9 100%); }}
#view-life .view-head {{ border-bottom: 1px solid #e8d4cf; }}
#view-life .arch {{ box-shadow: 0 24px 50px -30px rgba(140, 90, 90, .4); }}
#view-life .label {{ color: #9a7c82; }}
#view-life .shore {{ gap: 14px; column-gap: 14px; }}
#view-life .shore div {{ background: rgba(255, 255, 255, .72); border: 1px solid rgba(255, 255, 255, .95); border-radius: 18px; padding: 22px 24px; box-shadow: 0 14px 40px -34px rgba(140, 90, 90, .45); align-content: start; }}
#view-life .shore h3 {{ color: #3d3a35; }}
#view-life .shore p {{ color: #5f5850; }}

/* studies: soft golden gate */
#view-studies {{ min-height: 100vh; background: linear-gradient(180deg, #f3e7cb 0%, #f6ecd6 35%, #f7f0e2 70%, #f6f1e9 100%); }}
#view-studies .view-head {{ border-bottom: 1px solid #e6d7b8; }}
#view-studies .arch {{ box-shadow: 0 24px 50px -30px rgba(150, 100, 70, .4); }}
#view-studies .label {{ color: #9a7f55; }}
#view-studies .edu {{ background: rgba(255, 255, 255, .72); border: 1px solid rgba(255, 255, 255, .95); border-radius: 20px; padding: 28px 30px; box-shadow: 0 14px 40px -34px rgba(150, 100, 70, .45); }}
#view-studies .edu > p:last-child {{ color: #3d3a35; }}
#view-studies h3.sub {{ color: #3d3a35; }}
#view-studies .focus .card {{ background: rgba(255, 255, 255, .6); border: 1px solid rgba(255, 255, 255, .95); border-top: 2px solid #d9957b; border-radius: 4px 4px 18px 18px; padding: 20px 22px; }}
#view-studies .focus .card p {{ color: #5f5850; }}

#view-studies .project {{ background: rgba(255, 255, 255, .72); border: 1px solid rgba(255, 255, 255, .95); border-top: 2px solid #d9957b; border-radius: 4px 4px 20px 20px; padding: 28px 30px; display: grid; gap: 14px; box-shadow: 0 14px 40px -34px rgba(150, 100, 70, .45); }}
#view-studies .project h4 {{ margin: 0; font-family: var(--display); font-style: italic; font-weight: 400; font-size: 1.9rem; line-height: 1.15; }}
#view-studies .project p {{ color: #3d3a35; max-width: 62ch; }}
#view-studies .facts {{ margin: 6px 0 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; border-top: 1px solid #ecdcc4; padding-top: 16px; }}
#view-studies .facts dt {{ font-size: .66rem; letter-spacing: .24em; text-transform: uppercase; color: #9a7f55; }}
#view-studies .facts dd {{ margin: 4px 0 0; font-size: .95rem; color: #3d3a35; line-height: 1.5; }}
@media (max-width: 720px) {{ #view-studies .facts {{ grid-template-columns: minmax(0, 1fr); gap: 12px; }} #view-studies .project {{ padding: 22px 20px; }} }}

/* temple frames */
.frame {{ position: relative; width: 100%; }}
.frame .temple {{ position: absolute; left: -7%; top: -5.5%; width: 114%; height: 113%; pointer-events: none; overflow: visible; }}
.cards {{ padding-inline: 2%; column-gap: clamp(30px, 5vw, 64px); }}
.card-arch .frame {{ margin-bottom: 10px; }}
.about .about-frame {{ max-width: 420px; justify-self: center; }}
@media (max-width: 720px) {{ .cards {{ column-gap: 18px; padding-inline: 3%; }} .about .about-frame {{ max-width: 280px; }} }}

@keyframes fade {{ from {{ transform: translateY(10px); opacity: .01; }} to {{ transform: none; opacity: 1; }} }}

@media (max-width: 720px) {{
  .toplinks {{ gap: 16px; }}
  .intro {{ padding-block: 70px 40px; }}
  #mosaic {{ height: 230px; }}
  .cards {{ gap: 10px; }}
  .card-cap {{ display: none; }}
  .card-title {{ font-size: 1.15rem; margin-top: 8px; }}
  .about {{ grid-template-columns: minmax(0, 1fr); padding-block: 90px 20px; }}
  .about .arch {{ max-width: 280px; }}
  .view-head {{ grid-template-columns: 110px minmax(0, 1fr); align-items: center; }}
  .entry {{ grid-template-columns: minmax(0, 1fr); gap: 4px; }}
  .focus, .shore {{ grid-template-columns: minmax(0, 1fr); }}
}}
</style>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <filter id="blur05"><feGaussianBlur stdDeviation=".5"/></filter>
  <filter id="blur2" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="blur4" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="blur6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur10" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="10"/></filter>
  <filter id="frost"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .8 -.2"/></filter>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .4  0 0 0 0 .34  0 0 0 0 .26  0 0 0 .35 -.05"/></filter>
</svg>

<div id="home">
  <canvas id="mosaic" aria-hidden="true"></canvas>
  <div class="gutter">
    <div class="wrap">
      <nav class="topbar" aria-label="Main">
        <a class="mark" href="#">B. Brandau</a>
        <div class="toplinks">
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
          <a href="resume.pdf" target="_blank" rel="noopener">Résumé</a>
        </div>
      </nav>

      <header class="intro">
        <span class="label">Civil Engineering &amp; Philosophy · UC Berkeley</span>
        <h1>Brienna Brandau</h1>
        <svg class="wave-rule" viewBox="0 0 120 14" aria-hidden="true"><path d="M2,7 C12,1 22,1 32,7 S52,13 62,7 S82,1 92,7 S112,13 118,7" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
        <p class="lede">Bridges, big questions, and the beach.</p>
      </header>

      <nav class="cards" aria-label="Explore">{cards}
      </nav>
      <p class="note">three pieces from my collection, choose one</p>

      <section class="about" id="about">
        <div class="frame about-frame"><div class="arch">{about_arch}</div>{temple('t-about')}</div>
        <div class="about-text">
          <span class="label">About me</span>
          <h2>Hi, I'm Brie</h2>
          <p>I'm a civil engineering and philosophy student at UC Berkeley. On the engineering side, I'm most interested in where structures meet the Earth: foundations, coastlines, bridges, and the systems that keep cities running. Philosophy keeps me focused on the people behind every project. A seawall or a bridge changes how a whole community lives, works, and gets home at night, and I believe good engineering starts with listening to the people who will live with what we build.</p>
          <p>My experiences have each taught me something I'll bring to my work: break a messy problem into pieces, take safety seriously, and stay calm when everyone's waiting on you.</p>
        </div>
      </section>

      <section class="quote">
        <span class="label">On my desk</span>
        <blockquote>Sitting in the center of my desk is a clear jar of sea glass. Every piece was once dismissed as broken and worthless, until the tide softened its edges and carried it to shore. I study civil engineering to understand forces like that, slow and patient, and to build things that can stand up to them.</blockquote>
      </section>

      <section class="contact" id="contact">
        <span class="label">Say hello</span>
        <h2>Let's talk</h2>
        <p class="big">I'm looking for summer 2027 internships in civil engineering, infrastructure, and consulting. If your work touches the water, I'd especially love to hear about it.</p>
        <span class="email" id="email">brienna@berkeley.edu</span>
        <div class="links">
          <button class="textbtn" id="copy" type="button">Copy email</button>
          <a class="textbtn" href="https://www.linkedin.com/in/briennabrandau/" target="_blank" rel="noopener">LinkedIn</a>
          <a class="textbtn" href="resume.pdf" target="_blank" rel="noopener">Résumé</a>
        </div>
      </section>

      <footer>
        <span class="label">© <span id="yr">2026</span> Brienna Brandau</span>
        <span class="label">Collected in Berkeley</span>
      </footer>
    </div>
  </div>
</div>
{views}

<script>
  const VIEWS = ['experience', 'studies', 'life'];
  const home = document.getElementById('home');
  let last = null;
  function route() {{
    const key = location.hash.slice(1);
    const isView = VIEWS.includes(key);
    home.hidden = isView;
    VIEWS.forEach(v => document.getElementById('view-' + v).hidden = v !== key);
    if (isView) {{
      window.scrollTo(0, 0);
      const h = document.querySelector('#view-' + key + ' h2'); h.setAttribute('tabindex', '-1'); h.focus({{ preventScroll: true }});
    }} else if (key) {{
      const t = document.getElementById(key); if (t) t.scrollIntoView();
    }} else if (last) {{
      const c = document.querySelector('.card-arch[href="#' + last + '"]');
      if (c) c.scrollIntoView({{ block: 'center' }});
    }}
    last = isView ? key : null;
  }}
  addEventListener('hashchange', route); route();



  // stained sea glass band at the top, fading into the paper
  function drawMosaic() {{
    const c = document.getElementById('mosaic');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.round(c.clientWidth * dpr), h = Math.round(c.clientHeight * dpr);
    if (!w || !h) return;
    c.width = w; c.height = h;
    const ctx = c.getContext('2d');
    let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const pal = [[184,214,208],[201,226,221],[232,238,233],[214,196,160],[226,210,178],[170,200,190],[196,215,226],[218,228,212],[160,192,186],[236,226,208],[205,222,200]];
    const G = 64 * dpr, gx = Math.ceil(w / G) + 2, gy = Math.ceil(h / G) + 2, pts = [];
    for (let j = 0; j < gy; j++) for (let i = 0; i < gx; i++) {{
      pts.push({{ x: (i - 1 + rnd()) * G, y: (j - 1 + rnd()) * G, c: pal[Math.floor(rnd() * pal.length)], l: .9 + rnd() * .2, ox: rnd() * .6 - .3, oy: rnd() * .6 - .3 }});
    }}
    const img = ctx.createImageData(w, h), d = img.data, paper = [246, 241, 233], lead = 3.2 * dpr;
    for (let y = 0; y < h; y++) {{
      const fade = Math.min(1, Math.max(0, (y / h - .22) / .58)), f = fade * fade * (3 - 2 * fade);
      for (let x = 0; x < w; x++) {{
        const ci = Math.floor(x / G) + 1, cj = Math.floor(y / G) + 1;
        let b1 = 1e18, b2 = 1e18, best = null;
        for (let jj = cj - 1; jj <= cj + 1; jj++) for (let ii = ci - 1; ii <= ci + 1; ii++) {{
          const p = pts[jj * gx + ii]; if (!p) continue;
          const dx = x - p.x, dy = y - p.y, dd = dx * dx + dy * dy;
          if (dd < b1) {{ b2 = b1; b1 = dd; best = p; }} else if (dd < b2) b2 = dd;
        }}
        const edge = Math.sqrt(b2) - Math.sqrt(b1);
        let r, g, b;
        if (edge < lead) {{ const k = 1 - edge / lead; r = 236 - 12 * k; g = 229 - 12 * k; b = 216 - 14 * k; }}
        else {{
          const dx = (x - best.x) / G - best.ox, dy = (y - best.y) / G - best.oy;
          const light = best.l + .12 - Math.sqrt(dx * dx + dy * dy) * .22, grain = (rnd() - .5) * 6;
          const rim = Math.max(0, 1 - (edge - lead) / (5 * dpr)) * 14;
          r = best.c[0] * light + grain + rim; g = best.c[1] * light + grain + rim; b = best.c[2] * light + grain + rim;
        }}
        const o = (y * w + x) * 4;
        d[o] = r + (paper[0] - r) * f; d[o + 1] = g + (paper[1] - g) * f; d[o + 2] = b + (paper[2] - b) * f; d[o + 3] = 255;
      }}
    }}
    ctx.putImageData(img, 0, 0);
  }}
  let mw = 0, mt;
  function maybeDraw() {{ const c = document.getElementById('mosaic'); if (c.clientWidth && c.clientWidth !== mw) {{ mw = c.clientWidth; drawMosaic(); }} }}
  maybeDraw();
  addEventListener('resize', () => {{ clearTimeout(mt); mt = setTimeout(maybeDraw, 200); }});
  addEventListener('hashchange', () => setTimeout(maybeDraw, 0));

  const copyBtn = document.getElementById('copy'), emailEl = document.getElementById('email');
  copyBtn.addEventListener('click', () => {{
    const done = () => {{ copyBtn.textContent = 'Copied'; setTimeout(() => copyBtn.textContent = 'Copy email', 1600); }};
    const selectIt = () => {{ const r = document.createRange(); r.selectNodeContents(emailEl); const s = getSelection(); s.removeAllRanges(); s.addRange(r); copyBtn.textContent = 'Press ⌘/Ctrl+C'; }};
    try {{ navigator.clipboard.writeText(emailEl.textContent.trim()).then(done, selectIt); }} catch (e) {{ selectIt(); }}
  }});
  document.getElementById('yr').textContent = new Date().getFullYear();
</script>
'''
head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
i = html.index('</style>') + len('</style>')
open(os.path.join(ROOT, 'index.html'), 'w').write(head + html[:i] + '\n</head>\n<body>\n' + html[i:] + '</body>\n</html>\n')
print('Built index.html')
