#!/usr/bin/env python3
"""Build self-contained animated SVG artwork. Run with Python + fontTools."""
from pathlib import Path
import html
import math
import random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
FONT = TTFont(Path(__file__).parent / 'fonts/VG5000-Regular.ttf')
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UNITS = FONT['head'].unitsPerEm
VIOLET, CYAN, ORANGE, CHARCOAL, WHITE = '#730FFF', '#00EBFF', '#FF5A3C', '#414141', '#FFFFFF'

def group(body, attrs=''):
    return f'<g {attrs}>{body}</g>'

def text(x, y, value, size, color=WHITE):
    scale, advance, parts = size / UNITS, 0, []
    for char in value:
        glyph = GLYPHS[CMAP.get(ord(char), '.notdef')]
        pen = SVGPathPen(GLYPHS)
        glyph.draw(pen)
        if pen.getCommands():
            parts.append(f'<path d="{pen.getCommands()}" transform="translate({x+advance:.3f} {y}) scale({scale:.5f} {-scale:.5f})"/>')
        advance += glyph.width * scale
    return group(''.join(parts), f'fill="{color}" aria-label="{html.escape(value, quote=True)}"')

def rect(x,y,w,h,fill='none',stroke=None,sw=1,attrs=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '+(f'stroke="{stroke}" stroke-width="{sw}" ' if stroke else '')+attrs+'/>'

def path(d,color=WHITE,width=1,attrs=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {attrs}/>'

def line(x,y,xx,yy,color=WHITE,width=1,attrs=''):
    return path(f'M{x} {y}L{xx} {yy}',color,width,attrs)

def circle(x,y,r,color=WHITE,attrs=''):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}" {attrs}/>'

def cross(x,y,color):
    return line(x-6,y-6,x+6,y+6,color,2)+line(x-6,y+6,x+6,y-6,color,2)

def window(label,color=WHITE,w=1280):
    return rect(22,22,w-44,37,stroke=color)+text(37,48,label,19,color)+cross(w-41,40,color)

def save(name,body,height,bg,title,motion):
    # Still composition is the default. All temporal behavior is opt-in to the
    # visitor's no-preference media setting, including decorative visibility.
    style = '<style>@media (prefers-reduced-motion:no-preference){'+motion+'}</style>'
    desc = 'Original illustrative motion design; not live telemetry or measured results. Reduced-motion preferences show a still composition.'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{desc}</desc>{style}{rect(0,0,1280,height,bg)}{body}</svg>'
    (OUT / name.replace(".svg", "-motion.svg")).write_text(svg)
    (OUT / name).write_text(svg.replace(style, ""))

# 1. Hero: an exploded isometric system, a travelling map and a three-stage loop.
map_parts=[]
for row in range(-3,8):
    for col in range(-3,8):
        x,y=col*135,row*108
        for inset in range(4):
            pad=inset*7
            map_parts.append(rect(x+pad,y+pad,110-2*pad,83-2*pad,stroke=WHITE,sw=.7))
        map_parts.append(line(x+42,y,x+42,y+83,WHITE,.7))
b='<defs><clipPath id="map"><rect x="686" y="60" width="594" height="499"/></clipPath></defs>'
b+=group(group(group(''.join(map_parts),'transform="translate(820 70) rotate(28) skewX(-12)"'),'class="map-drift"'),'clip-path="url(#map)" opacity=".27"')
b+=window('AHAMED IN MOTION / PERSONAL ENGINEERING PORTFOLIO')
b+=text(44,223,'SYED',155)+text(43,381,'AHAMED',147)
b+=text(47,432,'Applied AI / Robotics / Systems',25)+text(47,478,'Abu Dhabi, UAE',23)
b+=rect(709,92,520,431,VIOLET,WHITE,1.5)+rect(709,92,520,35,WHITE)
b+=text(724,117,'SYSTEMS IN MOTION',19,VIOLET)+cross(1208,109,VIOLET)
b+=text(730,163,'01 / BUILD',16)+text(1079,163,'02 / TEST',16)
b+=text(729,453,'03 / ITERATE',16)+text(1090,453,'REPEAT',16)
# Stationary guide axes frame the animated exploded geometry.
b+=line(968,177,968,422,WHITE,1,attrs='opacity=".3" stroke-dasharray="3 8"')
b+=line(800,306,1136,306,WHITE,1,attrs='opacity=".2"')
for k,y in enumerate([227,277,327]):
    d=f'M968 {y-56}L1077 {y}L968 {y+56}L859 {y}Z'
    plate=path(d,WHITE,2)+line(968,y-56,968,y+56,WHITE,1,attrs='opacity=".3"')
    plate+=line(859,y,1077,y,WHITE,1,attrs='opacity=".3"')
    plate+=circle(968,y,4,WHITE)
    b+=group(plate,f'class="layer layer-{k}"')
# Packets travel up the system bus; these are decorative, not live status.
for k in range(3):
    b+=group(rect(963,352,10,10,WHITE),f'class="bus-packet" opacity="0" style="animation-delay:{-k*1.6}s"')
for k,label in enumerate(['BUILD','TEST','ITERATE']):
    x=729+k*161
    b+=rect(x,477,153,28,stroke=WHITE,attrs='opacity=".35"')
    b+=group(rect(x,477,153,28,WHITE),f'class="phase phase-{k}" opacity="0"')
    b+=text(x+12,497,label,17)
    b+=group(text(x+12,497,label,17,VIOLET),f'class="phase phase-{k}" opacity="0"')
b+=line(710,543,1227,543,WHITE,2,attrs='opacity=".28"')
b+=group(line(710,543,1227,543,WHITE,3),'class="cycle-progress" style="transform-origin:710px 543px"')
b+=line(24,564,1256,564)+text(45,600,'Software. Hardware. The people behind both.',23)+text(1176,600,'2026',21)
css='''
.map-drift{animation:mapDrift 28s ease-in-out infinite alternate}
@keyframes mapDrift{to{transform:translate(-40px,24px)}}
.layer{animation:layerFloat 6s ease-in-out infinite;transform-origin:968px 277px}
.layer-1{animation-delay:-2s}.layer-2{animation-delay:-4s}
@keyframes layerFloat{0%,100%{transform:translateY(-10px)}50%{transform:translateY(10px)}}
.bus-packet{animation:bus 4.8s linear infinite}
@keyframes bus{0%{transform:translateY(0);opacity:0}15%,75%{opacity:1}100%{transform:translateY(-175px);opacity:0}}
.phase{animation:phase 9s linear infinite}.phase-1{animation-delay:-6s}.phase-2{animation-delay:-3s}
@keyframes phase{0%,29%{opacity:1}33.333%,96%{opacity:0}100%{opacity:1}}
.cycle-progress{animation:progress 9s linear infinite}
@keyframes progress{0%{transform:scaleX(.02)}95%{transform:scaleX(1)}100%{transform:scaleX(.02)}}
'''
save('hero.svg',b,625,VIOLET,'Syed Ahamed — applied AI, robotics and systems. Build, test, iterate.',css)

# 2. Firasah: source nodes, graph traversal and a composed briefing.
b=window('01 / APPLIED INTELLIGENCE',CHARCOAL)+text(42,160,'Firasah',89,CHARCOAL)
b+=text(45,219,'From evidence to briefing.',27,CHARCOAL)+text(45,306,'Graph RAG / Cited retrieval / Artifacts',19,CHARCOAL)
pts=[(744,189),(818,119),(818,265),(910,185),(1000,118),(1000,263),(1077,185)]
for i,j in [(0,1),(0,2),(1,3),(2,3),(1,4),(3,4),(3,5),(2,5),(4,6),(5,6)]:
    x,y=pts[i];xx,yy=pts[j];b+=line(x,y,xx,yy,CHARCOAL,1.2,attrs='opacity=".42"')
route='M744 189L818 119L910 185L1000 263L1077 185L1143 185'
b+=path(route,CHARCOAL,3,attrs='class="traversal" pathLength="100" stroke-dasharray="9 91"')
for i,(x,y) in enumerate(pts):
    b+=rect(x-6,y-6,12,12,CHARCOAL)
    b+=group(rect(x-13,y-13,26,26,stroke=CHARCOAL,sw=2),f'class="node-ping" opacity=".4" style="animation-delay:{-i*.65}s;transform-origin:{x}px {y}px"')
b+=rect(1116,128,113,137,CYAN,CHARCOAL,2)+text(1130,151,'BRIEF',17,CHARCOAL)
for k,w in enumerate([79,79,60,72,43]):
    b+=group(line(1130,174+k*16,1130+w,174+k*16,CHARCOAL,3),f'class="brief-line" style="transform-origin:1130px {174+k*16}px;animation-delay:{-k*.25}s"')
b+=text(734,326,'ILLUSTRATIVE RETRIEVAL / NOT LIVE DATA',13,CHARCOAL)
css='''
.traversal{animation:traverse 6s linear infinite}@keyframes traverse{to{stroke-dashoffset:-100}}
.node-ping{animation:ping 5s ease-out infinite}@keyframes ping{0%,65%,100%{opacity:.2;transform:scale(.7)}25%{opacity:1;transform:scale(1.1)}}
.brief-line{animation:compose 6s ease-in-out infinite}@keyframes compose{0%,25%{transform:scaleX(.15);opacity:.3}55%,85%{transform:scaleX(1);opacity:1}100%{transform:scaleX(.15);opacity:.3}}
'''
save('firasah.svg',b,356,CYAN,'Firasah — evidence flows through a graph into a briefing. Illustrative retrieval.',css)

# 3. Himaya: three periodic conceptual traces and an event scanning line.
b=window('02 / PHYSICAL SYSTEMS')+text(42,160,'Himaya',89)
b+=text(45,219,'Three signals. One event.',27)+text(45,306,'Vibration / Acoustics / Rotation',19)
b+='<defs><clipPath id="scope"><rect x="823" y="86" width="406" height="209"/></clipPath></defs>'
for k,label in enumerate(['VIB','SOUND','RPM']):
    y=123+k*68
    b+=text(735,y+6,label,18)+line(823,y,1229,y,WHITE,1,attrs='opacity=".18"')
    points=[]
    for n in range(641):
        x=823+n*2
        phase=(n*2 % 420)/420
        envelope=math.exp(-((phase-.5)/.10)**2)
        a=(4+23*envelope)*math.sin(phase*math.tau*(15+k*8)) if k<2 else 5*math.sin(phase*math.tau)-24*envelope
        points.append(f'{x:.2f},{y+a:.2f}')
    trace=f'<polyline points="{" ".join(points)}" fill="none" stroke="{ORANGE}" stroke-width="2.3"/>'
    b+=group(group(trace,'class="scope-trace"'),'clip-path="url(#scope)"')
b+=group(rect(823,89,25,200,WHITE,attrs='opacity=".06"')+line(847,89,847,289,WHITE,1.2),'class="scope-scan"')
b+=text(735,326,'CONCEPTUAL SIGNALS / NOT TEST DATA',13)
css='''
.scope-trace{animation:traceFlow 7s linear infinite}@keyframes traceFlow{to{transform:translateX(-420px)}}
.scope-scan{animation:scopeScan 7s ease-in-out infinite}@keyframes scopeScan{0%,100%{transform:translateX(0);opacity:0}10%,80%{opacity:1}90%{transform:translateX(380px);opacity:0}}
'''
save('himaya.svg',b,356,CHARCOAL,'Himaya — three moving conceptual signals. Not test data.',css)

# 4. FlyBrain: topology is fixed while a pulse propagates from an intervention.
b=window('03 / EXPERIMENTAL SOFTWARE')+text(42,160,'FlyBrain Lab',79)
b+=text(45,219,'Intervene. Compare. Replay.',27)+text(45,306,'Circuits / Simulation / Reproducibility',19)
b+='<defs><clipPath id="network"><rect x="720" y="75" width="520" height="217"/></clipPath></defs>'
rng=random.Random(8)
pts=[(980+rng.uniform(-230,230),185+rng.uniform(-83,83)) for _ in range(64)]
network=''
for i,(x,y) in enumerate(pts):
    nearest=sorted(range(len(pts)),key=lambda j:(pts[j][0]-x)**2+(pts[j][1]-y)**2)[1:4]
    for j in nearest:
        if j>i:
            xx,yy=pts[j]
            network+=line(round(x,2),round(y,2),round(xx,2),round(yy,2),WHITE,.8,attrs='opacity=".36"')
for i,(x,y) in enumerate(pts):
    dist=math.hypot(x-976,y-185)
    network+=circle(x,y,4 if i%8==0 else 2.5,WHITE,f'class="neuron" style="animation-delay:{dist/100:.2f}s"')
for delay in [0,-3]:
    network+=group(circle(976,185,72,'none','stroke="#FFFFFF" stroke-width="1.8"'),f'class="ripple" opacity=".24" style="transform-origin:976px 185px;animation-delay:{delay}s"')
network+=path('M942 166V149H959M993 149H1010V166M1010 203V220H993M959 220H942V203',WHITE,2)
network+=circle(976,185,5)
b+=group(network,'clip-path="url(#network)"')+text(735,326,'ILLUSTRATIVE NETWORK / NOT ANATOMY',13)
css='''
.neuron{animation:neuralPulse 6s ease-in-out infinite}@keyframes neuralPulse{0%,12%,65%,100%{opacity:.4}30%,38%{opacity:1}}
.ripple{animation:ripple 6s ease-out infinite}@keyframes ripple{0%{transform:scale(.15);opacity:0}15%{opacity:.65}90%,100%{transform:scale(3);opacity:0}}
'''
save('flybrain.svg',b,356,VIOLET,'FlyBrain Lab — an illustrative circuit intervention and propagating activity. Not anatomy.',css)

# 5. Robotics: a sequence across the six curriculum ranks, not personal attainment.
b=window('42 ABU DHABI / ROBOTICS CLUB',CHARCOAL)+text(42,151,'Build. Document. Defend.',58,CHARCOAL)
b+=text(45,195,'Make engineering ability reproducible.',25,CHARCOAL)
for i,label in enumerate(['E','D','C','B','A','S']):
    x=44+i*199
    b+=rect(x,235,176,69,CHARCOAL)+text(x+19,285,label,43,ORANGE)
    if i<5:b+=text(x+128,278,'>',26,ORANGE)
    highlight=rect(x+3,238,170,63,ORANGE)+text(x+19,285,label,43,CHARCOAL)
    if i<5:highlight+=text(x+128,278,'>',26,CHARCOAL)
    b+=group(highlight,f'class="rank-step" opacity="0" style="animation-delay:{i*1.5}s"')
b+=line(45,321,1215,321,CHARCOAL,1,attrs='opacity=".3"')
b+=group(line(45,321,1215,321,CHARCOAL,3),'class="rank-progress" style="transform-origin:45px 321px"')
b+=text(45,360,'A six-rank cursus / Projects / Peer evaluation / Technical defences',18,CHARCOAL)
css='''
.rank-step{animation:rankStep 9s ease-in-out infinite}@keyframes rankStep{0%,2%,16.67%,100%{opacity:0}4%,13%{opacity:1}}
.rank-progress{animation:rankProgress 9s linear infinite}@keyframes rankProgress{0%{transform:scaleX(.02)}95%{transform:scaleX(1)}100%{transform:scaleX(.02)}}
'''
save('robotics.svg',b,389,ORANGE,'Robotics Club — six curriculum ranks, from projects to technical defences.',css)

# 6. Footer: the conversation arrow travels, while the invitation stays still.
b=window('CONTINUE THE CONVERSATION')+text(42,141,"Let's build something that works.",48)
b+=text(47,202,'AHAMED IN MOTION / APPLIED AI / ROBOTICS / SYSTEMS',21)
b+=group(path('M1141 141H1200M1178 119L1200 141L1178 163',WHITE,3),'class="next-arrow"')
css='.next-arrow{animation:next 3s ease-in-out infinite}@keyframes next{0%,100%{transform:translateX(-7px)}50%{transform:translateX(7px)}}'
save('footer.svg',b,232,VIOLET,'Ahamed in motion. Let us build something that works. Connect on LinkedIn.',css)
print('Built six self-contained motion SVGs with reduced-motion still compositions.')
