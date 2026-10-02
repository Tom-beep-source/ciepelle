# Pub « essayage » v2 : minutage calé sur la pub de référence (accroche 0-2,25 s, polaire 2,25-4,5 s, tenues 4,5-8,5 s, offre 8,5-10,5 s)
import json
BPM=120; B=60/BPM
HOOK=['Wyglądają jak zwykłe','*przezroczyste rajstopy*, ale…']
PROOF=['Ale…','to *ocieplane rajstopy z polarem*','na zimę']
OUT=['Idealne, żeby nosić','*lekkie stylizacje* tej zimy']
OFFER=['Im więcej par,','*tym więcej oszczędzasz*']   # vrai : 99 zł / 74,50 zł / 63 zł la paire selon le lot (220 g)
segs=[dict(clip='H1',src=2.4,speed=1.1,hand=.5,beats=4.5,zoom=1.0,lines=HOOK,zoom_out_to=1,cy=.42),
      dict(clip='VF',src=.6,speed=.8,hand=.4,beats=4.5,zoom=1.45,push=.05,cx=.48,cy=.48,soft=.72,lines=PROOF,pop=True,y=.2)]
def outfit(n,src,lines,first=False):   # un seul plan par tenue, gestes à peine accélérés : rythme posé
    return [dict(clip=n,src=src,speed=1.15,hand=.5,beats=2,zoom=1.0,lines=lines,pop=first)]
segs+=outfit('O1',.5,OUT,True)+outfit('O2',.75,OUT)+outfit('O5',.67,OUT)+outfit('O3',.8,OUT)
segs+=[dict(clip='O6',src=0,speed=1,hand=.5,beats=2,zoom=1.0,push=.05,lines=OFFER,pop=True)]+outfit('O4',.8,OFFER)
t=0
for s in segs:
    d=s['beats']*B; s['start']=round(t,4); s['end']=round(t+d,4); t+=d
cut=round(t,4)
tl=dict(bpm=BPM,dur=round(cut+2.0,2),fade_start=cut-.01,cut=cut,impact=cut,outside=cut+5,heels=[],snow_steps=[],segments=segs)
json.dump(tl,open('timeline.json','w'),indent=1,ensure_ascii=False); print(cut,tl['dur'])
