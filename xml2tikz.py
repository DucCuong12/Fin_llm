import sys, re, html, xml.etree.ElementTree as ET
from collections import defaultdict
src, out, FS = sys.argv[1], sys.argv[2], float(sys.argv[3])  # FS: font multiplier
U = 0.75  # pt per px
r = ET.parse(src).getroot()
cells = {c.get('id'): c for c in r.iter('mxCell')}
def style(c):
    d = {}
    for kv in (c.get('style') or '').split(';'):
        if '=' in kv:
            k, v = kv.split('=', 1); d[k] = v
    return d
UNI = {'√':r'$\surd$','Δ':r'$\Delta$','λ':r'$\lambda$','τ':r'$\tau$','α':r'$\alpha$','ρ':r'$\rho$','σ':r'$\sigma$','∈':r'$\in$','→':r'$\to$','·':r'$\cdot$',
       'ε':r'$\epsilon$','̃':'','̂':'','≥':r'$\geq$','≤':r'$\leq$','×':r'$\times$','−':'--','±':r'$\pm$','Σ':r'$\Sigma$','∑':r'$\sum$','‖':r'$\|$','μ':r'$\mu$','̄':''}
def esc(s):
    s = html.unescape(s)
    s = s.replace('\\', r'\textbackslash{}')
    for ch in '&%#_{}$':
        s = s.replace(ch, '\\' + ch)
    # combining marks: x + U+0303 / U+0302 / U+0304
    G = {'σ':r'\sigma','λ':r'\lambda','τ':r'\tau','μ':r'\mu','ρ':r'\rho','α':r'\alpha'}
    for mk, cmd in (('\u0303','tilde'),('\u0302','hat'),('\u0304','bar')):
        s = re.sub('(.)'+mk, lambda m, cmd=cmd: '$\\'+cmd+'{'+G.get(m.group(1),m.group(1))+'}$', s)
    s = s.replace('\\{', '{').replace('\\}', '}') if False else s
    for k, v in UNI.items(): s = s.replace(k, v)
    return s
def conv(v):
    v = v or ''
    # protect literal braces before tag handling
    toks = re.split(r'(<[^>]+>)', v)
    o = []
    for t in toks:
        m = re.match(r'<(/?)(\w+)', t)
        if m:
            c, n = m.groups()
            if n == 'b': o.append('}' if c else r'\textbf{')
            elif n == 'i': o.append('}' if c else r'\textit{')
            elif n == 'sub': o.append('}' if c else r'\textsubscript{')
            elif n == 'br': o.append(r'\\ ')
        else: o.append(esc(t))
    s = ''.join(o)
    s = s.replace('\\{', '\\{').replace('\\}', '\\}')
    return s
nodes = {}
for i, c in cells.items():
    g = c.find('mxGeometry')
    if c.get('vertex') and g is not None:
        nodes[i] = tuple(float(g.get(k)) for k in ('x', 'y', 'width', 'height'))
H = max(y + h for x, y, w, h in nodes.values()) + 10
def P(x, y): return f'({x*U/28.45:.4f},{(H-y)*U/28.45:.4f})'  # px -> cm, y flipped
col = lambda s, d: ('{rgb,255:red,%d;green,%d;blue,%d}' % tuple(int(s[k:k+2], 16) for k in (1, 3, 5))) if s and s.startswith('#') else d
L = [r'\documentclass[border=2pt]{standalone}', r'\usepackage[T1]{fontenc}', r'\usepackage{helvet,amsmath,amssymb,tikz}', r'\renewcommand{\familydefault}{\sfdefault}',
     r'\begin{document}', r'\begin{tikzpicture}[x=1cm,y=1cm]']
# edges bookkeeping: spread ports
edges = [c for c in cells.values() if c.get('edge')]
def side(a, b):  # a=src box, b=tgt box -> (sa, sb)
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    if ax + aw < bx: return 'R', 'L'
    if bx + bw < ax: return 'L', 'R'
    if ay + ah <= by: return 'B', 'T'
    return 'T', 'B'
plans = []
ports = defaultdict(list)
for e in edges:
    wp = [(float(p.get('x')), float(p.get('y'))) for p in e.iter('mxPoint')]
    a, b = nodes[e.get('source')], nodes[e.get('target')]
    if wp:
        s1 = 'B' if wp[0][1] > a[1] + a[3] else 'T'; s2 = 'T' if wp[-1][1] < b[1] else 'B'
    else: s1, s2 = side(a, b)
    plans.append((e, wp, s1, s2))
    ports[(e.get('source'), s1)].append(e.get('id')); ports[(e.get('target'), s2)].append(e.get('id'))
def port(nid, sd, eid):
    x, y, w, h = nodes[nid]; lst = ports[(nid, sd)]; k = lst.index(eid); n = len(lst); f = (k + 1) / (n + 1)
    return {'R': (x + w, y + h * f), 'L': (x, y + h * f), 'T': (x + w * f, y), 'B': (x + w * f, y + h)}[sd]
# nodes
for i, (x, y, w, h) in nodes.items():
    c = cells[i]; s = style(c); fs = float(s.get('fontSize', 12)) * U * FS
    dashed = 'dashed' if 'dashed' in s else ''
    fill = col(s.get('fillColor'), 'white') if s.get('fillColor', 'none') != 'none' else None
    rc = max(1, float(s.get('arcSize', 8)) * min(w, h) / 100) * U
    top = s.get('verticalAlign') == 'top'
    txt = conv(c.get('value'))
    if s.get('fontStyle') == '1': txt = r'\textbf{' + txt + '}'
    opt = f'draw={col(s.get("strokeColor"),"black")},{dashed},rounded corners={rc:.1f}pt,line width=0.8pt'
    if fill: opt += f',fill={fill}'
    if top:
        L.append(f'\\draw[{opt}] {P(x,y)} rectangle {P(x+w,y+h)};')
        L.append(f'\\node[anchor=north west,text width={(w-16)*U/28.45:.3f}cm,inner sep=0pt,font=\\fontsize{{{fs:.1f}}}{{{fs*1.15:.1f}}}\\selectfont] at {P(x+10,y+6)} {{{txt}}};')
    else:
        L.append(f'\\draw[{opt}] {P(x,y)} rectangle {P(x+w,y+h)};')
        tw = (w - 8) * U / 28.45
        L.append(f'\\node[text width={tw:.3f}cm,align=center,inner sep=0pt,font=\\fontsize{{{fs:.1f}}}{{{fs*1.15:.1f}}}\\selectfont] at {P(x+w/2,y+h/2)} {{{txt}}};')
# edges
for e, wp, s1, s2 in plans:
    sid, tid, eid = e.get('source'), e.get('target'), e.get('id')
    p1 = port(sid, s1, eid); p2 = port(tid, s2, eid); st = style(e)
    pts = [p1]
    if wp:
        # orthogonal: down from p1 to wp0.y, across, then to p2
        pts = [p1, (p1[0], wp[0][1]), (wp[-1][0], wp[0][1]), (wp[-1][0], p2[1])]
    else:
        if s1 in 'RL':
            if abs(p1[1] - p2[1]) < 1: pts = [p1, (p2[0], p1[1])]
            else: mx = (p1[0] + p2[0]) / 2; pts = [p1, (mx, p1[1]), (mx, p2[1]), p2]
        else:
            if abs(p1[0] - p2[0]) < 1: pts = [p1, (p1[0], p2[1])]
            else: my = (p1[1] + p2[1]) / 2; pts = [p1, (p1[0], my), (p2[0], my), p2]
    if wp and abs(pts[-1][0] - p2[0]) > 1: pts[-1] = (pts[-1][0], p2[1])
    d = 'dashed,' if 'dashed' in st else ''
    L.append(f'\\draw[{d}-latex,line width=0.9pt,draw={col(st.get("strokeColor"),"black")}] ' + ' -- '.join(P(*p) for p in pts) + ';')
    if e.get('value'):
        fs = float(st.get('fontSize', 12)) * U * FS * 0.9
        # label on longest segment
        segs = list(zip(pts, pts[1:])); a, b = max(segs, key=lambda sg: abs(sg[0][0]-sg[1][0]) + abs(sg[0][1]-sg[1][1]))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        vert = abs(a[0] - b[0]) < 1
        anc = 'west' if vert else 'south'; dx = 4 if vert else 0; dy = 0 if vert else -2
        L.append(f'\\node[anchor={anc},inner sep=1pt,fill=white,font=\\fontsize{{{fs:.1f}}}{{{fs*1.15:.1f}}}\\selectfont\\itshape] at {P(mx+dx,my+dy)} {{{conv(e.get("value"))}}};')
L += [r'\end{tikzpicture}', r'\end{document}']
open(out, 'w').write('\n'.join(L))
