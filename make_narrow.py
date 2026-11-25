# Generates narrow, vertical-flow draw.io diagrams sized for a 12.2 cm text column (1 px = 0.75 pt, 13 px ~ body text).
import re, math
from xml.sax.saxutils import quoteattr
FS = 11
COL = {'gray': ('#f5f5f5', '#666666'), 'blue': ('#dae8fc', '#6c8ebf'), 'orange': ('#ffe6cc', '#d79b00'),
       'green': ('#d5e8d4', '#82b366'), 'purple': ('#e1d5e7', '#9673a6')}
def nlines(v, w):
    n = 0
    for ln in v.split('<br>'):
        t = re.sub('<[^>]+>', '', ln); t = re.sub('&[a-z#0-9]+;', 'x', t)
        n += max(1, math.ceil(len(t) * 5.9 / (w - 10)))
    return n
class G:
    def __init__(s, W): s.W, s.cells, s.i = W, [], 1
    def box(s, x, y, w, v, col, h=None, extra=''):
        s.i += 1; h = h or nlines(v, w) * 14 + 12
        f, k = COL[col]
        st = f'rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor={f};strokeColor={k};fontFamily=Helvetica;fontSize={FS};{extra}'
        s.cells.append(f'<mxCell id="n{s.i}" value={quoteattr(v)} style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return f'n{s.i}', y + h
    def group(s, x, y, w, h, title, k):
        s.i += 1
        st = f'rounded=1;whiteSpace=wrap;html=1;arcSize=3;dashed=1;fillColor=none;strokeColor={k};verticalAlign=top;align=left;spacingLeft=8;fontStyle=1;fontFamily=Helvetica;fontSize={FS};'
        s.cells.insert(0, f'<mxCell id="n{s.i}" value={quoteattr(title)} style="{st}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    def edge(s, a, b, label='', dashed=False):
        s.i += 1
        st = f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeColor=#333333;fontFamily=Helvetica;fontSize={FS};' + ('dashed=1;' if dashed else '')
        s.cells.append(f'<mxCell id="e{s.i}" value={quoteattr(label)} style="{st}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    def save(s, f, name, H):
        open(f, 'w').write(f'<mxfile host="app.diagrams.net"><diagram id="{name}" name="{name}"><mxGraphModel dx="800" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{s.W}" pageHeight="{H}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(s.cells) + '</root></mxGraphModel></diagram></mxfile>')
# ---------- overview ----------
g = G(460); w = 195
p, y1 = g.box(0, 0, w, '<b>Market prices</b><br>adjusted close p<sub>i,t</sub>', 'gray')
n, _ = g.box(265, 0, w, '<b>Company news</b><br>articles x &isin; X<sub>i,t</sub>', 'gray')
v, y2 = g.box(0, 70, w, '<b>Volatility budget</b> &lambda;<sub>t</sub> &isin; [0, 1]<br>price only, no LLM<br><i>how much risk to hold</i><br>scale portfolio to a 20% volatility target', 'blue', h=120)
t, _ = g.box(265, 70, w, '<b>Event tilt</b> &tau;<sub>i,t</sub> &isin; [0.5, 1.5]<br>LLM event scorer<br><i>where to allocate the risk</i><br>cross-sectional rank of event scores', 'orange', h=120)
e, y3 = g.box(110, 250, 240, '<b>Exposure</b><br>w<sub>i,t</sub> = &lambda;<sub>t</sub> &middot; &tau;<sub>i,t</sub><br>long-only, never levered', 'green')
o, y4 = g.box(110, y3 + 40, 240, '<b>Portfolio</b><br>position at close t earns t&rarr;t+1<br>5 bps turnover cost', 'purple')
g.edge(p, v); g.edge(n, t); g.edge(t, v, 'lagged tilt', True); g.edge(v, e); g.edge(t, e); g.edge(e, o)
g.save('method_overview.xml', 'VolTilt overview', y4)
# ---------- detailed ----------
g = G(460); bw = 195; gap = 18
L = ['<b>1. News articles</b><br>x &isin; X<sub>i,t</sub><br>dated, no intraday time',
     '<b>2. LLM event extractor g</b><br>JSON schema, temperature 0<br>focus, type, novelty,<br>hard_numbers,<br>impact &isin; {-2..+2}<br>cached per article',
     '<b>3. Hard-number gate</b><br>keep only focus = main subject<br>and hard_numbers = true',
     '<b>4. Daily score and smoothing</b><br>h<sub>i,t</sub> = sum of kept impacts<br>s<sub>i,t</sub> = &alpha; h<sub>i,t</sub> + (1-&alpha;) s<sub>i,t-1</sub><br>&alpha; = 2/21 (span 20 days)',
     '<b>5. Rank tilt &tau;<sub>i,t</sub></b><br>1 + k (&rho; - &rho;&#772;) / ((n-1)/2)<br>k = 0.5, mean tilt = 1<br>n &lt; 3: tilt off (&tau; = 1)']
R = ['<b>A. Prices and returns</b><br>r<sub>i,t</sub> = p<sub>i,t</sub> / p<sub>i,t-1</sub> - 1<br>live set A<sub>t</sub>',
     "<b>B. Tilted portfolio return</b><br>r&#771;<sub>t</sub> = mean<sub>i</sub> (&tau;<sub>i,t-1</sub> &middot; r<sub>i,t</sub>)<br>uses yesterday's tilt",
     '<b>C. Realised volatility</b><br>&sigma;&#770;<sub>t</sub> = &radic;P &middot; std of the last<br>20 days of r&#771;',
     '<b>D. Volatility budget</b><br>&lambda;<sub>t</sub> = min(1, 20% / &sigma;&#770;<sub>t</sub>)<br>&lambda; = 1 until 20 days exist']
top = 0
def col(x, items, c):
    y = top; ids = []
    for v in items:
        i, y2 = g.box(x, y, bw, v, c); ids.append(i); y = y2 + gap
    for a, b in zip(ids, ids[1:]): g.edge(a, b)
    return ids, y - gap
li, ly = col(0, L, 'orange'); ri, ry = col(265, R, 'blue')
bot = max(ly, ry)
f, fy = g.box(80, bot + 36, 300, '<b>E. Exposure and execution</b><br>w<sub>i,t</sub> = &lambda;<sub>t</sub> &middot; &tau;<sub>i,t</sub>, long-only, never levered<br>position at close t earns t&rarr;t+1, cost 5 bps &middot; |&Delta;w|', 'green')
g.edge(li[-1], f, 'tilt'); g.edge(ri[-1], f, 'budget')
g.edge(li[-1], ri[1], '', True)
xy = fy
g.save('method_detailed.xml', 'VolTilt pipeline', xy)
