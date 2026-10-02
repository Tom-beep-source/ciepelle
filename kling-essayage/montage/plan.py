# Pub « essayage » Ciepelle : accroche -> preuve polaire -> tenues en coupes rapides -> offre réelle -> logo
import json
BPM=120; B=60/BPM
HOOK=['Wyglądają jak zwykłe','*cienkie rajstopy*, ale…']
PROOF=['Ale…','to *rajstopy z polarem*','na zimę']
OUT=['Idealne do *lekkich stylizacji*','tej zimy']
OFFER=['*Zestaw 3 par*','już od 149 zł']          # offre réelle : 3 paires 80 g = 149 zł
segs=[
 dict(clip='H1',src=0.2,speed=1,beats=5,zoom=1.0,lines=HOOK,pop=False),
 dict(clip='VF',src=.4, speed=1,beats=4,zoom=1.0,push=.14,lines=PROOF,pop=True,y=.235),
 dict(clip='O1',src=.2, speed=1,beats=2,zoom=1.0,lines=OUT,pop=True),
 dict(clip='O2',src=.2, speed=1,beats=2,zoom=1.0,lines=OUT),
 dict(clip='O5',src=.2, speed=1,beats=2,zoom=1.0,lines=OUT),
 dict(clip='O3',src=.2, speed=1,beats=2,zoom=1.0,lines=OUT),
 dict(clip='O6',src=0,  speed=1,beats=2,zoom=1.0,push=.05,lines=OFFER,pop=True),
 dict(clip='O4',src=.2, speed=1,beats=2,zoom=1.0,lines=OFFER),
]
t=0
for s in segs:
    d=s['beats']*B; s['start']=round(t,4); s['end']=round(t+d,4); t+=d
cut=round(t,4)
tl=dict(bpm=BPM,dur=round(cut+2.3,2),fade_start=cut-.01,cut=cut,impact=cut,outside=cut+5,heels=[],snow_steps=[],segments=segs)
json.dump(tl,open('timeline.json','w'),indent=1,ensure_ascii=False); print(cut, tl['dur'])
