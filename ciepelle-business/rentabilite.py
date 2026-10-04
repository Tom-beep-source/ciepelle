# Graphique de rentabilité par commande Ciepelle. Lancer : python3 rentabilite.py
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
EUR=4.37
PRIX,ACHAT,TVA,FRAIS=145.4,57.1,27.2,11.7   # commande moyenne (mix de ventes supposé), frais = paiement 3 % + retours 5 %
MARGE=PRIX-ACHAT-TVA-FRAIS                  # 49,5 zł avant pub
FIXE=148                                    # Shopify Basic ~39 $ + domaine, par mois
S,TXT,TXT2,MUT,GRID='#fcfcfb','#0b0b0b','#52514e','#898781','#e1e0d9'
BLUE,ORANGE,AQUA,YEL='#2a78d6','#eb6834','#1baf7a','#eda100'
GOOD,CRIT='#0ca30c','#d03b3b'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':TXT,'axes.labelcolor':TXT2,
  'xtick.color':MUT,'ytick.color':MUT,'axes.edgecolor':GRID,'figure.facecolor':S,'axes.facecolor':S})
def z(x): return f"{x:.0f} zł".replace('-','−')
fig,ax=plt.subplots(3,1,figsize=(9,15.5),gridspec_kw={'height_ratios':[1,1.05,1.15],'hspace':.55})
fig.suptitle("Ciepelle : combien te rapporte une commande ?",x=.06,ha='left',fontsize=17,fontweight='bold')
fig.text(.06,.935,"Commande moyenne : "+z(PRIX)+f" ({PRIX/EUR:.1f} €)".replace('.',',')+" · Marge avant pub : "+z(MARGE)+f" ({MARGE/EUR:.1f} €)".replace('.',',')+"\nTaux : 1 € = 4,37 zł · Avec TVA polonaise 23 %",ha='left',color=TXT2,fontsize=10.5)
# A. décomposition
a=ax[0]; cas=[(30,'Pub à 30 zł / vente\n(bonne vidéo)'),(40,'Pub à 40 zł / vente\n(objectif)'),(70,'Pub à 70 zł / vente\n(moyenne du secteur)')]
for i,(cpa,lab) in enumerate(cas):
    y=2-i; x=0
    for v,c,n in [(ACHAT,BLUE,'Achat + livraison'),(TVA,ORANGE,'TVA'),(FRAIS,AQUA,'Frais + retours'),(cpa,YEL,'Pub')]:
        a.barh(y,v-1,left=x,color=c,height=.62,edgecolor=S,linewidth=2); 
        a.text(x+v/2,y,f"{v:.0f}",ha='center',va='center',fontsize=10,color='white' if c in (BLUE,ORANGE) else TXT)
        x+=v
    res=PRIX-x
    if res>=0:
        a.barh(y,res-1,left=x,color=GOOD,height=.62); a.text(x+res+2,y,f"+{res:.0f} zł gagnés",va='center',color=GOOD,fontweight='bold')
    else:
        a.text(x+2,y,f"{z(res)} perdus",va='center',color=CRIT,fontweight='bold')
a.axvline(PRIX,color=TXT2,lw=1.2,ls='--'); a.text(PRIX,2.45,f"Prix payé\n{PRIX:.0f} zł".replace('.',','),ha='center',fontsize=9,color=TXT2)
a.set_yticks([2,1,0]); a.set_yticklabels([l for _,l in cas],color=TXT); a.set_xlim(0,215); a.set_ylim(-.5,3.0)
a.set_title("1. Où va l'argent d'une commande",loc='left',fontweight='bold',pad=26)
hs=[plt.Rectangle((0,0),1,1,color=c) for c in (BLUE,ORANGE,AQUA,YEL,GOOD)]
a.legend(hs,['Achat + livraison','TVA','Frais + retours','Pub','Bénéfice'],ncol=5,loc='lower left',bbox_to_anchor=(0,1.0),frameon=False,fontsize=9,handlelength=1)
a.set_xlabel('zł'); 
# B. bénéfice par commande selon coût pub
b=ax[1]; xs=list(range(0,121)); b.plot(xs,[MARGE-x for x in xs],color=BLUE,lw=2.5)
b.axhline(0,color=TXT2,lw=1); b.fill_between(xs,[MARGE-x for x in xs],0,where=[x<=MARGE for x in xs],color=GOOD,alpha=.12); b.fill_between(xs,[MARGE-x for x in xs],0,where=[x>=MARGE for x in xs],color=CRIT,alpha=.10)
b.plot([MARGE],[0],'o',ms=10,color=TXT,markeredgecolor=S,markeredgewidth=2)
b.annotate(f"Point mort : {MARGE:.0f} zł ({MARGE/EUR:.1f} €) de pub par vente".replace('.',','),(MARGE,0),(MARGE+12,38),fontweight='bold',arrowprops=dict(arrowstyle='-',color=TXT2))
for cpa,lab in [(30,'bonne vidéo'),(40,'objectif'),(70,'moyenne secteur'),(100,'mauvais')]:
    v=MARGE-cpa; b.plot([cpa],[v],'o',ms=8,color=BLUE,markeredgecolor=S,markeredgewidth=2)
    b.text(cpa+2,v+(4 if v>0 else -9),f"{lab} : {'+' if v>0 else ''}{z(v)}",fontsize=9.5,color=TXT)
b.text(3,-45,"Zone de perte",color=CRIT,fontsize=10,fontweight='bold'); b.text(3,8,"Zone de gain",color=GOOD,fontsize=10,fontweight='bold')
b.set_xlim(0,120); b.set_ylim(-75,60); b.grid(color=GRID,lw=.6); b.set_axisbelow(True)
for s in ('top','right'): b.spines[s].set_visible(False)
b.set_xlabel("Coût de la pub pour obtenir 1 vente (zł)"); b.set_ylabel("Bénéfice par commande (zł)")
b.set_title("2. Bénéfice par commande selon le coût de la pub",loc='left',fontweight='bold')
# C. bénéfice du mois selon nb de ventes
c=ax[2]; n=list(range(0,61))
for cpa,col,lab in [(30,BLUE,'Pub à 30 zł / vente'),(40,ORANGE,'Pub à 40 zł / vente'),(70,AQUA,'Pub à 70 zł / vente')]:
    ys=[k*(MARGE-cpa)-FIXE for k in n]; c.plot(n,ys,color=col,lw=2.2,label=lab)
    c.text(61,ys[-1],f"{lab}\n{'+' if ys[-1]>0 else ''}{ys[-1]:.0f} zł".replace('-','−'),va='center',fontsize=9,color=TXT)
    if MARGE>cpa:
        be=FIXE/(MARGE-cpa); c.plot([be],[0],'o',ms=9,color=col,markeredgecolor=S,markeredgewidth=2)
        c.annotate(f"rentable dès\n{int(be)+1} ventes/mois",(be,0),(be+(-2 if cpa==30 else 6),330 if cpa==30 else -420),fontsize=9.5,fontweight='bold',arrowprops=dict(arrowstyle='-',color=TXT2))
c.axhline(0,color=TXT2,lw=1); c.grid(color=GRID,lw=.6); c.set_axisbelow(True)
for s in ('top','right'): c.spines[s].set_visible(False)
c.set_xlim(0,60); c.set_xlabel("Nombre de ventes dans le mois"); c.set_ylabel("Bénéfice du mois (zł)")
c.set_title(f"3. Bénéfice du mois (après {FIXE} zł de frais fixes Shopify + domaine)",loc='left',fontweight='bold')
c.legend(loc='upper left',frameon=False,fontsize=9.5)
fig.text(.06,.015,"Estimations. Mix de ventes supposé : 25 % 1 paire, 45 % 2 paires, 15 % 3 paires, 15 % Trio ; 30 % 80 g, 50 % 220 g, 20 % 300 g.\nCoûts fournisseurs relevés le 4 octobre 2026 (prix publics AliExpress). Sans TVA (franchise), la marge monte d'environ 27 zł.",color=MUT,fontsize=8.5)
plt.savefig('rentabilite-par-commande.png',dpi=130,bbox_inches='tight',facecolor=S)
