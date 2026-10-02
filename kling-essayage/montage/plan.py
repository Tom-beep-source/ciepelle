# Pub « essayage » : structure reprise de Le Collant Frenchie (accroche -> preuve polaire -> tenues en coupes rapides -> offre)
import json
BPM=120; B=60/BPM
segs=[
 dict(clip='H1',src=0.2,speed=1,beats=5,zoom=1.0,text='Wyglądają jak cienkie rajstopy…',size=54,pop=False),
 dict(clip='VF',src=.4, speed=1,beats=4,zoom=1.0,push=.14,text='…ale w środku mają polar.',pop=True),
 dict(clip='O1',src=.3, speed=1,beats=2,zoom=1.0,text='Lekkie stylizacje nawet zimą',size=56,pop=True),
 dict(clip='O2',src=.3, speed=1,beats=2,zoom=1.0,text='Lekkie stylizacje nawet zimą',size=56,pop=False),
 dict(clip='O3',src=.3, speed=1,beats=2,zoom=1.0,text='Lekkie stylizacje nawet zimą',size=56,pop=False),
 dict(clip='O4',src=.3, speed=1,beats=2,zoom=1.0,text='Lekkie stylizacje nawet zimą',size=56,pop=False),
]
t=0
for s in segs:
    d=s['beats']*B; s['start']=round(t,4); s['end']=round(t+d,4); t+=d
cut=round(t,4)
tl=dict(bpm=BPM,dur=round(cut+2.6,2),fade_start=cut-.01,cut=cut,impact=cut,outside=cut+5,heels=[],snow_steps=[],segments=segs)
json.dump(tl,open('timeline.json','w'),indent=1,ensure_ascii=False); print(cut, tl['dur'])
