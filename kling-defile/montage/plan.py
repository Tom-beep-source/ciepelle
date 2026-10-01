# Plan de montage calé sur le tempo : chaque coupe tombe sur un temps, chaque talon détecté devient un clic
import json
BPM=126; B=60/BPM; LAT=-0.03          # LAT : le clic part au contact du talon, un peu avant le point bas du pied
# poses de talon mesurées dans chaque clip (clips/*.mp4, s) - V1/V2/V3 détection auto vérifiée à l'image, VS relevé à l'image
STRIKES={'V1':[.71,1.67,2.54,3.46,4.42],'V2':[.71,1.67,2.62,3.58,4.42],'V3':[.75,1.79,2.75,3.79,4.75]}
VS_HEEL=[2.55,3.30]; VS_SNOW=[4.05,4.75]
segs=[ # clip, point d'entrée dans le clip (s), durée en temps
 dict(clip='V1',src=.234, beats=4, text='Wyglądają jak gołe nogi…'),
 dict(clip='VF',src=.50,  beats=4, text='…a w środku polar.'),
 dict(clip='V1',src=2.984,beats=4, label='Cielisty'),
 dict(clip='V2',src=.234, beats=4, label='Czarny'),
 dict(clip='V3',src=.274, beats=4, label='Szary'),
 dict(clip='VS',src=2.25, dur=2.75, text='A za drzwiami…', text2='zima.'),
]
t=0; heels=[]; snow=[]
for s in segs:
    s['start']=round(t,4); d=s.get('dur',s.get('beats',0)*B); s['end']=round(t+d,4)
    for x in STRIKES.get(s['clip'],[]):
        tt=t+x-s['src']
        if t<=tt<t+d-.05: heels.append(round(tt+LAT,4))
    if s['clip']=='VS':
        heels+=[round(t+x-s['src']+LAT,4) for x in VS_HEEL]; snow=[round(t+x-s['src'],4) for x in VS_SNOW]
        s['text2_at']=round(t+3.45-s['src'],4)   # elle franchit le seuil
    t+=d
cut=round(t,4); hit=round(cut+.2,4)
tl=dict(bpm=BPM,dur=round(hit+2.55,2),fade_start=segs[-1]['start'],cut=cut,impact=hit,outside=segs[-1]['text2_at'],
        heels=heels,snow_steps=snow,segments=segs)
json.dump(tl,open('timeline.json','w'),indent=1,ensure_ascii=False); print(json.dumps({k:v for k,v in tl.items() if k!='segments'}))
