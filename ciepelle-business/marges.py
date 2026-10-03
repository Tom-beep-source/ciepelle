# Marges Ciepelle : 27 déclinaisons + 3 Trio, à partir de couts-fournisseurs.json. Écrit marges.md.
import json
C=json.load(open('couts-fournisseurs.json')); usd=C['taux']['usd_pln']; eur=C['taux']['eur_pln']
PRIX={'80':{1:79,2:119,3:149},'220':{1:99,2:149,3:189},'300':{1:119,2:179,3:229}}
TRIO={'80':149,'220':189,'300':229}
def marge(prix,cout_usd,paires,tva):
    achat=(cout_usd+C['livraison_usd_par_paire']*paires)*usd
    ht=prix/(1+tva); m=ht-achat-prix*(C['frais_pct']+C['retours_pct'])
    return achat,m
def z(x): return f"{x:.0f} zł ({x/eur:.1f} €)".replace('.',',')
L=[]
etat=lambda k:'✅ relevés' if C[k]['releve'] else '⚠️ ESTIMATIONS, pas encore relevées'
L.append(f"# Marges par déclinaison\n\nCoûts Stone's Store : {etat('stones_store')} · Coûts COZOK (Trio) : {etat('cozok_trio')}\n")
L.append("Marge = prix (hors TVA) − achat fournisseur − livraison − 3 % de frais de paiement − 5 % de provision pour retours. **Avant publicité.**\n")
L.append("| Déclinaison | Prix | Achat + livraison | Marge avec TVA 23 % | Marge sans TVA (franchise) |\n|---|---|---|---|---|")
for n in (1,2,3):
  for col in ('Cielisty','Czarny','Szary'):
    for g in ('80','220','300'):
      p=PRIX[g][n]; c=C['stones_store'][col][g]*n
      a,m1=marge(p,c,n,C['tva_pl']); _,m0=marge(p,c,n,0)
      L.append(f"| {n} {'para' if n==1 else 'pary'} · {col} · {g} g | {p} zł | {z(a)} | **{z(m1)}** | {z(m0)} |")
L.append("\n## Zestaw Trio (1 chair + 1 noir + 1 gris, chez COZOK)\n\n| Trio | Prix | Achat + livraison | Marge avec TVA 23 % | Marge sans TVA |\n|---|---|---|---|---|")
for g in ('80','220','300'):
    p=TRIO[g]; c=sum(C['cozok_trio'][k][g] for k in ('Cielisty','Czarny','Szary'))
    a,m1=marge(p,c,3,C['tva_pl']); _,m0=marge(p,c,3,0)
    L.append(f"| Trio {g} g | {p} zł | {z(a)} | **{z(m1)}** | {z(m0)} |")
open('marges.md','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
