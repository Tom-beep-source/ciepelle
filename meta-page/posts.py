# Visuels des premiers posts de la page Ciepelle (1080x1350, format 4:5), à partir de nos propres images IA
from PIL import Image, ImageDraw, ImageFont, ImageOps
A='../kling-defile/assets/'; SERIF=A+'DMSerifDisplay-Regular.ttf'; SANS=A+'Manrope.ttf'
CREAM=(251,246,242); INK=(34,27,31); ROSE=(181,84,111); BERRY=(122,41,68)
W,H=1080,1350
def F(p,s,w=None):
    f=ImageFont.truetype(p,s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
def logo(s,color=INK):
    w,h=int(196*s),int(44*s); im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); lw=max(2,int(2.2*s))
    d.arc([(22-14)*s,(20-14)*s,(22+14)*s,(20+14)*s],90,270,fill=color,width=lw)
    d.arc([(22-7.5)*s,(20-7.5)*s,(22+7.5)*s,(20+7.5)*s],90,270,fill=ROSE,width=lw)
    r=2.6*s; d.ellipse([22*s-r,20*s-r,22*s+r,20*s+r],fill=ROSE)
    d.text((42*s,30*s),'Ciepelle',font=F(SERIF,int(27*s)),fill=color,anchor='ls'); return im.crop(im.getbbox())
def fit(path,w,h,cy=.5):
    im=Image.open(path).convert('RGB'); return ImageOps.fit(im,(w,h),Image.LANCZOS,centering=(.5,cy))
def base(): return Image.new('RGBA',(W,H),CREAM+(255,))
def foot(c,text='purrpeak.com'):
    d=ImageDraw.Draw(c); L=logo(1.25); c.alpha_composite(L,(60,H-60-L.height))
    d.text((W-60,H-60),text,font=F(SANS,28,500),fill=INK,anchor='rs')

# Post 2 : les 3 couleurs (tenues d'essayage, cadrées sur les jambes)
c=base(); d=ImageDraw.Draw(c)
d.text((60,70),'Który kolor wybierasz?',font=F(SERIF,64),fill=INK)
pw,ph=310,930
for i,(src,lab) in enumerate([('../kling-essayage/O1.png','Cielisty'),('../kling-essayage/O2.png','Czarny'),('../kling-essayage/O5.png','Szary')]):
    x=60+i*(pw+15); c.paste(fit(src,pw,ph,.62),(x,190))
    d.text((x+pw/2,190+ph+45),lab.upper(),font=F(SANS,32,700),fill=BERRY,anchor='ma')
foot(c); c.convert('RGB').save('posts/post2-3-kolory.jpg',quality=92)

# Post 4 : le polaire de l'intérieur (gros plan)
c=base(); d=ImageDraw.Draw(c)
c.paste(fit('../kling-defile/Fb.png',W,980,.45),(0,0))
d.text((60,1030),'Tak wyglądają od środka',font=F(SERIF,60),fill=INK)
d.text((60,1112),'Miękki polar w środku, cienki efekt na zewnątrz.',font=F(SANS,32,500),fill=BERRY)
foot(c); c.convert('RGB').save('posts/post4-polar.jpg',quality=92)

# Post 5 : Zestaw Trio (les 3 défilés)
c=base(); d=ImageDraw.Draw(c)
d.text((60,70),'Zestaw Trio',font=F(SERIF,72),fill=INK)
d.text((60,162),'Cielisty + czarny + szary w jednym zamówieniu',font=F(SANS,32,500),fill=BERRY)
pw,ph=310,860
for i,src in enumerate(['../kling-defile/W1a.png','../kling-defile/W2.png','../kling-defile/W3.png']):
    c.paste(fit(src,pw,ph,.55),(60+i*(pw+15),240))
pill=Image.new('RGBA',(430,84),(0,0,0,0)); ImageDraw.Draw(pill).rounded_rectangle([0,0,429,83],radius=42,fill=BERRY+(255,))
ImageDraw.Draw(pill).text((215,42),'3 pary od 149 zł',font=F(SANS,38,700),fill=CREAM,anchor='mm'); c.alpha_composite(pill,((W-430)//2,1130))
foot(c); c.convert('RGB').save('posts/post5-trio.jpg',quality=92)

# Post 6 : comment choisir l'épaisseur (carte typographique sur fond de polaire)
c=base(); d=ImageDraw.Draw(c)
d.text((60,70),'Jak wybrać grubość?',font=F(SERIF,68),fill=INK)
rows=[('80 g','Jesień','Chłodne dni, biuro, wieczór w mieście'),('220 g','Zima','Uniwersalna grubość na co dzień'),('300 g','Mrozy','Na najzimniejsze dni stycznia')]
y=230
for g,sez,txt in rows:
    d.rounded_rectangle([60,y,W-60,y+270],radius=28,fill=(244,234,226))
    d.text((110,y+70),g,font=F(SERIF,96),fill=BERRY,anchor='ls' if False else 'la')
    d.text((420,y+75),sez,font=F(SANS,46,700),fill=INK)
    d.text((420,y+145),txt,font=F(SANS,30,500),fill=INK)
    y+=300
d.text((60,1150),'Każda grubość w 3 kolorach: cielisty, czarny, szary.',font=F(SANS,32,500),fill=BERRY)
foot(c); c.convert('RGB').save('posts/post6-grubosc.jpg',quality=92)
