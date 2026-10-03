# Marges Ciepelle : 27 déclinaisons + 3 Trio, à partir de couts-fournisseurs.json (coûts en zł). Écrit marges.md.
import json
C=json.load(open('couts-fournisseurs.json')); eur=C['taux']['eur_pln']; L_=C['livraison']
PRIX={'80':{1:79,2:119,3:149},'220':{1:99,2:149,3:189},'300':{1:119,2:179,3:229}}
TRIO={'80':149,'220':189,'300':229}
def marge(prix,achat_pln,tva):
    liv=0 if achat_pln>=L_['gratuite_des_pln'] else L_['sinon_pln']
    achat=achat_pln+liv
    ht=prix/(1+tva); m=ht-achat-prix*(C['frais_pct']+C['retours_pct'])
    return achat,m
def z(x): return f"{x:.0f} zł ({x/eur:.1f} €)".replace('.',',')
L=[f"# Marges par déclinaison\n\nCoûts relevés le {C['releve_le']} sur AliExpress (prix public, prudent ; le prix DSers est en général un peu plus bas). Livraison AliExpress gratuite dès {L_['gratuite_des_pln']} zł d'achat, sinon ~{L_['sinon_pln']:.0f} zł.\n",
   "Marge = prix hors TVA − achat − livraison − 3 % de frais de paiement − 5 % de provision pour retours. **Avant publicité.** Deux colonnes : avec TVA polonaise 23 % (si tu dois la reverser) et sans TVA (franchise en base, à confirmer avec un comptable).\n",
   "| Déclinaison | Prix | Achat + livraison | Marge avec TVA 23 % | Marge sans TVA |\n|---|---|---|---|---|"]
rows=[]
for n in (1,2,3):
  for col in ('Cielisty','Czarny','Szary'):
    for g in ('80','220','300'):
      p=PRIX[g][n]; c=C['stones_store'][col][g]*n
      a,m1=marge(p,c,C['tva_pl']); _,m0=marge(p,c,0); rows.append((m1,f"{n}×{col} {g} g"))
      L.append(f"| {n} {'para' if n==1 else 'pary'} · {col} · {g} g | {p} zł | {z(a)} | **{z(m1)}** | {z(m0)} |")
L.append("\n## Zestaw Trio (1 chair + 1 noir + 1 gris, chez COZOK)\n\n| Trio | Prix | Achat + livraison | Marge avec TVA 23 % | Marge sans TVA |\n|---|---|---|---|---|")
for g in ('80','220','300'):
    p=TRIO[g]; c=sum(C['cozok_trio'][k][g] for k in ('Cielisty','Czarny','Szary'))
    a,m1=marge(p,c,C['tva_pl']); _,m0=marge(p,c,0); rows.append((m1,f"Trio {g} g"))
    L.append(f"| Trio {g} g | {p} zł | {z(a)} | **{z(m1)}** | {z(m0)} |")
rows.sort()
L.append(f"\n**Marge la plus faible (avec TVA) :** {rows[0][1]} = {z(rows[0][0])}. **La plus forte :** {rows[-1][1]} = {z(rows[-1][0])}.")
open('marges.md','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
