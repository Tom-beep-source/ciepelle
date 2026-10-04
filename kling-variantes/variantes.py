# 5 variantes de pub (TikTok / Reels / Meta), toutes en polonais, à partir des extraits existants.
# Usage : python3 variantes.py A  -> écrit montage/timeline.json pour la variante A
import json, sys
V=sys.argv[1]; BPM={'A':120,'B':126,'C':120,'D':116,'E':132,'F':120,'G':116,'H':120}[V]; B=60/BPM
def seg(clip,src,beats,lines=None,**k):
    d=dict(clip=clip,src=src,speed=k.pop('speed',1),beats=beats,zoom=k.pop('zoom',1.0),hand=k.pop('hand',.5),lines=lines,pop=k.pop('pop',True)); d.update(k); return d
FLEECE=dict(zoom=1.45,push=.05,cx=.48,cy=.48,soft=.72,speed=.8,hand=.4,y=.2)
OFFER=['Im więcej par,','*tym więcej oszczędzasz*']
OFFER2=['2 pary za *149 zł*','darmowa dostawa']
if V=='A':   # « Zimą w sukience? » : question d'accroche -> secret polaire -> tenues
    S=[seg('V1',.25,4,['Sukienka zimą','i *nie marzniesz*?'],pop=False),
       seg('VF',.6,4,['Sekret?','*Polar w środku.*'],**FLEECE),
       seg('O1',.5,2,['Wyglądają jak','*cienkie rajstopy*'],speed=1.15),
       seg('O2',.75,2,['Wyglądają jak','*cienkie rajstopy*'],speed=1.15,pop=False),
       seg('O5',.67,2,['Wyglądają jak','*cienkie rajstopy*'],speed=1.15,pop=False),
       seg('O4',.8,2,OFFER,speed=1.15)]
elif V=='B': # « 3 kolory » : défilé chair / noir / gris, puis preuve
    S=[seg('V1',.25,4,['Jeden model.','*Trzy kolory.*'],pop=False),
       seg('V1',2.98,3,None,label='Cielisty'),
       seg('V2',.23,3,None,label='Czarny'),
       seg('V3',.27,3,None,label='Szary'),
       seg('VF',.6,4,['A w środku','*miękki polar*'],**FLEECE),
       seg('O6',0,3,['Który kolor','*wybierasz?*'],push=.05)]
elif V=='C': # « POV » natif TikTok
    S=[seg('H1',2.4,4,['POV: wszyscy myślą,','że masz *gołe nogi*'],pop=False,speed=1.1),
       seg('VF',.6,4,['…a ty masz','*polar w środku*'],**FLEECE),
       seg('V2',.23,3,['80 g · 220 g · 300 g','*3 kolory*']),
       seg('O3',.8,2,OFFER,speed=1.15),
       seg('O5',.67,2,OFFER,speed=1.15,pop=False)]
elif V=='D': # « Za oknem zima » : la sortie dans la neige en ouverture
    S=[seg('VS',2.4,6,['Za oknem zima…','*a ona w cienkich rajstopach?*'],pop=False),
       seg('VF',.6,4,['To nie są zwykłe rajstopy.','*W środku polar.*'],**FLEECE),
       seg('O1',.5,2,['Sukienki i spódnice','*nawet zimą*'],speed=1.15),
       seg('O3',.8,2,['Sukienki i spódnice','*nawet zimą*'],speed=1.15,pop=False),
       seg('O4',.8,2,OFFER,speed=1.15)]
elif V=='E': # version courte et rapide (~7 s) : polaire d'abord, puis 6 tenues
    S=[seg('VF',.6,3,['To *nie są* zwykłe','rajstopy'],pop=False,**{k:v for k,v in FLEECE.items() if k!='y'},y=.2),
       seg('O1',.5,1,['Polar w środku,','*efekt gołych nóg*'],speed=1.3),
       seg('O2',.75,1,['Polar w środku,','*efekt gołych nóg*'],speed=1.3,pop=False),
       seg('O5',.67,1,['Polar w środku,','*efekt gołych nóg*'],speed=1.3,pop=False),
       seg('O3',.8,1,['Polar w środku,','*efekt gołych nóg*'],speed=1.3,pop=False),
       seg('O6',0,1,OFFER,push=.04),
       seg('O4',.8,1,OFFER,speed=1.3,pop=False)]
elif V=='F': # « Pincement » : le geste qui prouve que ce n'est pas la peau, en accroche
    S=[seg('P1',0,3,['Gołe nogi zimą?','*Nie – to rajstopy.*'],pop=False,push=.10,cx=.4,cy=.55,y=.2),
       seg('P2',0,2,['Gołe nogi zimą?','*Nie – to rajstopy.*'],pop=False,push=.10,cx=.6,cy=.45,y=.2),
       seg('VF',.6,3,['A w środku','*miękki polar*'],**FLEECE),
       seg('VS',2.4,4,['Sukienka *nawet zimą*'],pop=False),
       seg('O1',.5,2,OFFER2,speed=1.15),
       seg('O4',.8,2,OFFER2,speed=1.15,pop=False)]
elif V=='G': # Défilé corrigé : la sortie dans la neige en ouverture, prix à la fin
    S=[seg('VS',2.4,6,['Za oknem zima…','*a ona w cienkich rajstopach?*'],pop=False),
       seg('VF',.6,3,['…a w środku','*miękki polar.*'],**FLEECE),
       seg('V1',2.98,2,None,label='Cielisty'),
       seg('V2',.23,2,None,label='Czarny'),
       seg('V3',.27,2,None,label='Szary'),
       seg('V1',.25,3,OFFER2)]
elif V=='H': # Essayage corrigé : polaire plus courte, offre exacte du lien (2 pary 220 g)
    S=[seg('H1',.2,4,['Wyglądają jak zwykłe','*przezroczyste rajstopy*, ale…'],pop=False),
       seg('VF',.6,3,['…to rajstopy','*z polarem* na zimę'],**FLEECE),
       seg('O1',.5,2,['Lekkie stylizacje','*nawet zimą*'],speed=1.15),
       seg('O2',.75,2,['Lekkie stylizacje','*nawet zimą*'],speed=1.15,pop=False),
       seg('O3',.8,2,['Lekkie stylizacje','*nawet zimą*'],speed=1.15,pop=False),
       seg('O5',.67,2,OFFER2,speed=1.15),
       seg('O4',.8,2,OFFER2,speed=1.15,pop=False)]
t=0
for s in S:
    d=s['beats']*B; s['start']=round(t,4); s['end']=round(t+d,4); t+=d
cut=round(t,4)
for x in S:
    if x['clip']=='VS': x['text2_at']=round(x['start']+(3.45-x['src'])/x['speed'],4)   # moment où elle passe la porte
outside=S[0]['start']+(3.45-2.4) if V in 'DG' else cut+5     # D : le vent se lève quand elle sort
NEW=V in 'FGH'
tl=dict(offer='2 pary za 149 zł · darmowa dostawa' if NEW else 'Zestaw 3 par już od 149 zł',end_speed=.55 if NEW else 1.0,bpm=BPM,dur=round(cut+(1.3 if NEW else 2.0),2),fade_start=cut-.01,cut=cut,impact=cut,outside=outside,heels=[],snow_steps=[],segments=S)
json.dump(tl,open('montage/timeline.json','w'),indent=1,ensure_ascii=False); print(V,'durée',tl['dur'],'s')
