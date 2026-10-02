# Plan de montage « dynamique » : 150 BPM, une coupe tous les 2 temps (0,8 s), alternance plan large / plan serré,
# marche légèrement accélérée pour que chaque pas tombe sur un temps ; chaque talon détecté devient un clic
import json
BPM=150; B=60/BPM; LAT=-0.03
STRIKES={'V1':[.71,1.67,2.54,3.46,4.42],'V2':[.71,1.67,2.62,3.58,4.42],'V3':[.75,1.79,2.75,3.79,4.75]}
SPEED={'V1':0.93/(2*B),'V2':0.955/(2*B),'V3':1.0/(2*B)}   # période de pas mesurée -> 2 temps
VS_HEEL=[2.55,3.30]; VS_SNOW=[4.05,4.75]
def walk(clip,strike,label=None,text=None,first=False):
    sp=SPEED[clip]; src=strike-sp*B          # le pas `strike` tombe sur le 2e temps
    return [dict(clip=clip,src=src,speed=sp,beats=2,zoom=1.0,label=label,text=text,pop=not first and True),
            dict(clip=clip,src=src+sp*2*B,speed=sp,beats=2,zoom=1.45,label=label,text=text,pop=False)]
segs=(walk('V1',.71,text='Wyglądają jak gołe nogi…',first=True)
     +[dict(clip='VF',src=.4,speed=1,beats=4,zoom=1.0,push=.14,text='…a w środku polar.',pop=True)]
     +walk('V1',2.54,label='Cielisty')+walk('V2',.71,label='Czarny')+walk('V3',.75,label='Szary')
     +[dict(clip='VS',src=2.2,speed=1,beats=7,zoom=1.0,text='A za drzwiami…',text2='zima.',pop=True)])
segs[0]['pop']=False
t=0; heels=[]; snow=[]
for s in segs:
    d=s['beats']*B; s['start']=round(t,4); s['end']=round(t+d,4)
    for x in STRIKES.get(s['clip'],[]):
        tt=t+(x-s['src'])/s['speed']
        if t<=tt<t+d-.03 and round(tt,3) not in [round(h-LAT,3) for h in heels]: heels.append(round(tt+LAT,4))
    if s['clip']=='VS':
        heels+=[round(t+x-s['src']+LAT,4) for x in VS_HEEL]; snow=[round(t+x-s['src'],4) for x in VS_SNOW]
        s['text2_at']=round(t+3.45-s['src'],4)
    t+=d
cut=round(t,4); hit=round(cut+.15,4)
tl=dict(bpm=BPM,dur=round(hit+2.35,2),fade_start=segs[-1]['start'],cut=cut,impact=hit,outside=segs[-1]['text2_at'],
        heels=sorted(set(heels)),snow_steps=snow,segments=segs)
json.dump(tl,open('timeline.json','w'),indent=1,ensure_ascii=False); print(json.dumps({k:v for k,v in tl.items() if k!='segments'}))
