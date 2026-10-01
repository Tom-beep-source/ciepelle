# Animatique 1080x1920 30 fps : plans fixes animés (Ken Burns) + textes + logo final, synchronisé sur la bande-son
import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS,DUR=1080,1920,30,16.0
A='../assets/'; R='../../references-ciepelle/'; K='../'
SERIF=A+'DMSerifDisplay-Regular.ttf'; SANS=A+'Manrope.ttf'
CREAM=(251,246,242); INK=(34,27,31); ROSE=(181,84,111)
def font(p,s,w=None):
    f=ImageFont.truetype(p,s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
def cover(img,zoom):
    iw,ih=img.size; s=max(W/iw,H/ih)*zoom
    return img.resize((int(iw*s)+1,int(ih*s)+1),Image.LANCZOS)
def kenburns(img,p,z0=1.04,z1=1.12,dx=0,dy=-0.02):
    z=z0+(z1-z0)*p; im=cover(img,z); iw,ih=im.size
    cx=(iw-W)/2+dx*p*W; cy=(ih-H)/2+dy*p*H
    return im.crop((int(cx),int(cy),int(cx)+W,int(cy)+H))
def logo(scale, color=CREAM):
    # reproduit snippets/logo.liquid (viewBox 196x44)
    w,h=int(196*scale),int(44*scale); im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=scale; lw=max(2,int(2.2*s))
    d.arc([ (22-14)*s,(20-14)*s,(22+14)*s,(20+14)*s ],90,270,fill=color,width=lw)
    d.arc([ (22-7.5)*s,(20-7.5)*s,(22+7.5)*s,(20+7.5)*s ],90,270,fill=ROSE,width=lw)
    r=2.6*s; d.ellipse([22*s-r,20*s-r,22*s+r,20*s+r],fill=ROSE)
    f=font(SERIF,int(27*s)); d.text((42*s,30*s),'Ciepelle',font=f,fill=color,anchor='ls')
    return im.crop(im.getbbox())  # recadré sur le dessin réel pour un centrage exact
def text_layer(lines, y, size, alpha=1.0, spacing=1.15, weight=700, upper=False, track=0):
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay); f=font(SANS,size,weight)
    for i,l in enumerate(lines):
        l=l.upper() if upper else l
        if track:
            widths=[d.textlength(c,font=f) for c in l]; tw=sum(widths)+track*(len(l)-1); x=(W-tw)/2
            for c,wc in zip(l,widths):
                d.text((x,y+i*size*spacing),c,font=f,fill=CREAM+(int(255*alpha),)); x+=wc+track
        else:
            d.text((W/2,y+i*size*spacing),l,font=f,fill=CREAM+(int(255*alpha),),anchor='ma')
    sh=lay.split()[3].filter(ImageFilter.GaussianBlur(9)).point(lambda v:min(255,int(v*.9)))
    sh2=lay.split()[3].filter(ImageFilter.GaussianBlur(2)).point(lambda v:int(v*.45))
    shadow=Image.new('RGBA',(W,H),(20,14,17,0)); shadow.putalpha(sh)
    s2=Image.new('RGBA',(W,H),(20,14,17,0)); s2.putalpha(sh2)
    return Image.alpha_composite(Image.alpha_composite(shadow,s2),lay)
def snow(t,seed=3,n=420):
    rng=np.random.default_rng(seed); lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x0=rng.uniform(0,W,n); y0=rng.uniform(-H,H,n); sp=rng.uniform(90,260,n); r=rng.uniform(1.5,5.5,n); ph=rng.uniform(0,6.28,n)
    for i in range(n):
        y=(y0[i]+sp[i]*t)%(H+40)-20; x=x0[i]+18*math.sin(t*1.3+ph[i])
        d.ellipse([x-r[i],y-r[i],x+r[i],y+r[i]],fill=(255,255,255,int(150+90*(r[i]/5.5))))
    return lay.filter(ImageFilter.GaussianBlur(0.8))
def grain(im,amt=10,seed=0):
    a=np.asarray(im).astype(np.int16); n=np.random.default_rng(seed).normal(0,amt,(H,W,1)).astype(np.int16)
    return Image.fromarray(np.clip(a+n,0,255).astype(np.uint8))
# --- plans (placeholders là où la vidéo Kling viendra)
I=lambda p: Image.open(p).convert('RGB')
shots=[ # (debut, fin, image, texte, label, zoom/dir)
 (0.00, 2.00, I(K+'W1a.png'), ['Wyglądają jak','gołe nogi…'], None),
 (2.00, 3.60, I(K+'Fa.png'),  ['…a w środku','polar.'], None),
 (3.60, 6.00, I(K+'W1b.png'), None, 'Cielisty'),
 (6.00, 8.50, I(R+'06.jpg'),  None, 'Czarny'),
 (8.50,11.00, I(R+'12.jpg'),  None, 'Szary'),
 (11.00,13.25,I(K+'W1a.png'), ['A za drzwiami…','zima.'], None),
]
small=logo(2.2)
small_sh=Image.new('RGBA',small.size,(20,14,17,0)); small_sh.putalpha(small.split()[3].filter(ImageFilter.GaussianBlur(6)).point(lambda v:int(v*.8)))

proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-i','../audio/bande-son-defile.m4a','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-shortest','animatique-defile.mp4'],stdin=subprocess.PIPE)
for fi in range(int(DUR*FPS)):
    t=fi/FPS
    if t<13.25:
        s=[x for x in shots if x[0]<=t<x[1]][0]; p=(t-s[0])/(s[1]-s[0])
        fr=kenburns(s[2],p).convert('RGBA')
        if s[0]>=11.0:   # sortie dans la neige (placeholder) : la lumière se refroidit + neige
            cool=Image.new('RGBA',(W,H),(170,195,230,int(90*p))); fr=Image.alpha_composite(fr,cool); fr=Image.alpha_composite(fr,snow(t))
        if s[3]:
            a=min(1,(t-s[0])/0.18); fr=Image.alpha_composite(fr,text_layer(s[3],int(H*0.40),86,a))
        if s[4]:
            a=min(1,(t-s[0])/0.15)*min(1,(s[1]-t)/0.15); fr=Image.alpha_composite(fr,text_layer([s[4]],int(H*0.56),62,a,weight=700,upper=True,track=16))
        # petit logo en haut (zone sûre: sous les 14 % du haut)
        fr.alpha_composite(small_sh,((W-small.width)//2,int(H*0.155))); fr.alpha_composite(small,((W-small.width)//2,int(H*0.155)))
        fr=grain(fr.convert('RGB'),6,fi)
    elif t<13.45:
        fr=Image.new('RGB',(W,H),(0,0,0))
    else:
        tp=t-13.45
        bg=Image.new('RGBA',(W,H),INK+(255,))
        if tp<0.07: bg=Image.new('RGBA',(W,H),(70,58,64,255))   # flash sourd au moment de l'impact
        sc=4.4*(1+0.30*math.exp(-tp/0.07)); L=logo(sc)
        blur=10*math.exp(-tp/0.05)
        if blur>0.4: L=L.filter(ImageFilter.GaussianBlur(blur))
        sh=(int(10*math.exp(-tp/0.09)*math.sin(tp*90)), int(8*math.exp(-tp/0.09)*math.cos(tp*77)))
        bg.alpha_composite(L,((W-L.width)//2+sh[0],int(H*0.44)-L.height//2+sh[1]))
        a=min(1,max(0,(tp-0.45)/0.35))
        if a>0: bg=Image.alpha_composite(bg,text_layer(['Rajstopy z polarem'],int(H*0.52),40,a,weight=500,upper=True,track=10))
        a2=min(1,max(0,(tp-0.85)/0.35))
        if a2>0: bg=Image.alpha_composite(bg,text_layer(['80 g · 220 g · 300 g'],int(H*0.565),36,a2*.8,weight=400))
        fr=grain(bg.convert('RGB'),4,fi)
    proc.stdin.write(np.asarray(fr,dtype=np.uint8).tobytes())
proc.stdin.close(); proc.wait(); print('ok')
