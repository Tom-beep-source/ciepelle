# Montage final 1080x1920 24 fps : vrais plans Kling + textes + logo, calé sur timeline.json (plan.py) et la bande-son (audio/music.py)
import json, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,24
A='../assets/'; C='../clips/'
SERIF=A+'DMSerifDisplay-Regular.ttf'; SANS=A+'Manrope.ttf'
CREAM=(251,246,242); INK=(34,27,31); ROSE=(181,84,111)
TL=json.load(open('timeline.json')); SEGS=TL['segments']; CUT=TL['cut']; HIT=TL['impact']; DUR=TL['dur']

def font(p,s,w=None):
    f=ImageFont.truetype(p,s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
def logo(scale, color=CREAM):
    # reproduit snippets/logo.liquid (viewBox 196x44), recadré sur le dessin réel pour un centrage exact
    w,h=int(196*scale),int(44*scale); im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=scale; lw=max(2,int(2.2*s))
    d.arc([(22-14)*s,(20-14)*s,(22+14)*s,(20+14)*s],90,270,fill=color,width=lw)
    d.arc([(22-7.5)*s,(20-7.5)*s,(22+7.5)*s,(20+7.5)*s],90,270,fill=ROSE,width=lw)
    r=2.6*s; d.ellipse([22*s-r,20*s-r,22*s+r,20*s+r],fill=ROSE)
    d.text((42*s,30*s),'Ciepelle',font=font(SERIF,int(27*s)),fill=color,anchor='ls')
    return im.crop(im.getbbox())
def with_shadow(im,blur=7,k=.85):
    pad=blur*3; out=Image.new('RGBA',(im.width+2*pad,im.height+2*pad),(0,0,0,0))
    a=Image.new('L',out.size,0); a.paste(im.split()[3],(pad,pad)); a=a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*k))
    sh=Image.new('RGBA',out.size,(20,14,17,0)); sh.putalpha(a); out=Image.alpha_composite(out,sh); out.alpha_composite(im,(pad,pad)); return out
# --- étiquette de texte : bandeau encre arrondi, texte crème (style natif Reels, lisible sur toutes les images)
def caption(parts, size=60, track=0, upper=False, ink=INK):
    """parts = [(texte, alpha)] sur une ligne ; la largeur est celle du texte complet, pour qu'un mot ajouté ne fasse pas sauter le bandeau"""
    f=font(SANS,size,700); tmp=ImageDraw.Draw(Image.new('L',(1,1)))
    parts=[(p.upper() if upper else p,a) for p,a in parts]
    def tw(s): return sum(tmp.textlength(c,font=f) for c in s)+track*max(0,len(s)-1) if track else tmp.textlength(s,font=f)
    full=''.join(p for p,_ in parts); px,py=34,22
    asc,desc=f.getmetrics(); bw=int(tw(full)+2*px); bh=int(asc*.78+2*py+size*.18)
    im=Image.new('RGBA',(bw,bh),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,bw-1,bh-1],radius=22,fill=ink+(222,))
    x=px; base=py+asc*.78
    for p,a in parts:                    # chaque morceau sur son propre calque : un alpha < 1 doit s'estomper, pas trouer le bandeau
        lay=Image.new('RGBA',im.size,(0,0,0,0)); dl=ImageDraw.Draw(lay)
        if track:
            for c in p:
                dl.text((x,base),c,font=f,fill=CREAM+(255,),anchor='ls'); x+=tmp.textlength(c,font=f)+track
        else:
            dl.text((x,base),p,font=f,fill=CREAM+(255,),anchor='ls'); x+=tmp.textlength(p,font=f)
        if a<1: lay.putalpha(lay.split()[3].point(lambda v:int(v*a)))
        im=Image.alpha_composite(im,lay)
    return im
def pop(im,p):
    """apparition : léger zoom 0,94 -> 1 et fondu sur 0,14 s"""
    e=1-(1-min(1,max(0,p)))**3; s=.94+.06*e
    out=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
    if e<1: out.putalpha(out.split()[3].point(lambda v:int(v*e)))
    return out
def place_c(fr,im,cy):
    fr.alpha_composite(im,((W-im.width)//2,int(cy-im.height/2)))
def grain(arr,amt,seed):
    n=np.random.default_rng(seed).normal(0,amt,(H,W,1)).astype(np.int16)
    return np.clip(arr.astype(np.int16)+n,0,255).astype(np.uint8)

CAP_Y=int(H*.245)                       # bandeau texte : sous les 14 % du haut masqués par les Reels, au-dessus des 35 % du bas
def badge(scale=1.45):
    # petit logo permanent dans une pastille encre : lisible sur jupe beige, mur clair ou cheveux
    L=logo(scale); px,py=26,16; im=Image.new('RGBA',(L.width+2*px,L.height+2*py),(0,0,0,0))
    ImageDraw.Draw(im).rounded_rectangle([0,0,im.width-1,im.height-1],radius=im.height//2,fill=INK+(200,))
    im.alpha_composite(L,(px,py)); return im
small=badge(); SMALL_Y=int(H*.142)

class Clip:
    def __init__(s,name): s.cap=cv2.VideoCapture(C+name+'.mp4'); s.n=int(s.cap.get(cv2.CAP_PROP_FRAME_COUNT)); s.last=-1; s.cache={}
    def raw(s,i):
        i=max(0,min(i,s.n-1))
        if i in s.cache: return s.cache[i]
        if i<s.last or i>s.last+12: s.cap.set(cv2.CAP_PROP_POS_FRAMES,i); s.last=i-1   # sinon lecture séquentielle
        while s.last<i:
            ok,f=s.cap.read(); s.last+=1
            f=cv2.cvtColor(f,cv2.COLOR_BGR2RGB); h,w=f.shape[:2]; k=max(W/w,H/h)
            f=cv2.resize(f,(round(w*k),round(h*k)),interpolation=cv2.INTER_LANCZOS4)
            y=(f.shape[0]-H)//2; x=(f.shape[1]-W)//2; s.cache[s.last]=f[y:y+H,x:x+W]
            for k_ in [k_ for k_ in s.cache if k_<s.last-3]: del s.cache[k_]
        return s.cache[i]
    def at(s,src):
        """image au temps src (s) ; entre deux images, fondu pondéré (la marche accélérée reste fluide)"""
        f=src*FPS; i=int(math.floor(f)); w=f-i
        if w<.25: return s.raw(i)
        if w>.75: return s.raw(i+1)
        return (s.raw(i)*(1-w)+s.raw(i+1)*w).astype(np.uint8)
def zoomed(arr,z,cy=.5):
    if z<=1.001: return arr
    cw,ch=W/z,H/z; x0=(W-cw)/2; y0=min(max(cy*H-ch/2,0),H-ch)
    return cv2.resize(arr[int(y0):int(y0+ch),int(x0):int(x0+cw)],(W,H),interpolation=cv2.INTER_CUBIC)
clips={n:Clip(n) for n in {s['clip'] for s in SEGS}}

proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-i','../audio/bande-son-defile.m4a','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',
  '-c:a','copy','-shortest','-movflags','+faststart','defile-master.mp4'],stdin=subprocess.PIPE)
NF=int(round(DUR*FPS))
for fi in range(NF):
    t=fi/FPS
    if t<CUT:
        s=[x for x in SEGS if x['start']<=t+1e-6<x['end']+1e-6][0]
        lt=t-s['start']; src=s['src']+lt*s['speed']; arr=clips[s['clip']].at(src)
        z=s['zoom']*(1+s.get('push',0)*lt/(s['end']-s['start']))
        if s['start']>0: z*=1+.04*math.exp(-lt/.09)            # coup de zoom sur chaque coupe, qui se pose en 0,2 s
        arr=zoomed(arr,z,.64 if s['zoom']>1 else .5)
        fr=Image.fromarray(arr).convert('RGBA')
        fr.alpha_composite(small,((W-small.width)//2,SMALL_Y))
        if s.get('text'):
            p=(t-s['start'])/.14 if s.get('pop') else 1        # 1re image et suite d'un même texte : déjà plein
            if 'text2' in s:
                a2=min(1,max(0,(t-s['text2_at'])/.12))
                im=caption([(s['text']+' ',1),(s['text2'],a2)])
            else: im=caption([(s['text'],1)],size=s.get('size',60))
            place_c(fr,pop(im,p),CAP_Y)
        if s.get('label'):
            place_c(fr,pop(caption([(s['label'],1)],size=46,track=12,upper=True),(t-s['start']-.04)/.14 if s.get('pop') else 1),CAP_Y)
        arr=np.asarray(fr.convert('RGB'))
        if s['clip']=='VS':                 # dehors c'est l'hiver : la lumière se refroidit légèrement à mesure qu'elle sort
            k=min(1,max(0,(t-s['text2_at']+.6)/1.4))*.6
            arr=np.clip(arr*np.array([1-.06*k,1-.015*k,1+.05*k]),0,255).astype(np.uint8)
        arr=grain(arr,4,fi)
    elif t<HIT:
        arr=np.zeros((H,W,3),np.uint8)
    else:
        tp=t-HIT; bg=Image.new('RGBA',(W,H),INK+(255,))
        if tp<1/FPS: bg=Image.new('RGBA',(W,H),(74,60,67,255))      # flash sourd sur l'image de l'impact
        sc=5.0*(1+.32*math.exp(-tp/.07)); L=logo(sc)
        b=10*math.exp(-tp/.05)
        if b>.4: L=L.filter(ImageFilter.GaussianBlur(b))
        sx=int(10*math.exp(-tp/.09)*math.sin(tp*90)); sy=int(8*math.exp(-tp/.09)*math.cos(tp*77))
        bg.alpha_composite(L,((W-L.width)//2+sx,(H-L.height)//2+sy))   # centre exact de l'image
        lh=logo(5.0).height
        a=min(1,max(0,(tp-.45)/.35)); a2=min(1,max(0,(tp-.85)/.35))
        if a>0:
            f=font(SANS,46,500); lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
            txt='RAJSTOPY Z POLAREM'; tr=10; ws=[d.textlength(c,font=f) for c in txt]; x=(W-(sum(ws)+tr*(len(txt)-1)))/2
            for c,wc in zip(txt,ws): d.text((x,H/2+lh/2+70),c,font=f,fill=CREAM+(int(255*a),),anchor='ls'); x+=wc+tr
            if a2>0:
                ob=caption([('Zestaw 3 par już od 149 zł',1)],size=54,ink=ROSE)   # offre réelle de la boutique (3 paires 80 g)
                ob.putalpha(ob.split()[3].point(lambda v:int(v*a2))); lay.alpha_composite(ob,((W-ob.width)//2,int(H/2+lh/2+130)))
            bg=Image.alpha_composite(bg,lay)
        arr=grain(np.asarray(bg.convert('RGB')),3,fi)
    proc.stdin.write(arr.tobytes())
proc.stdin.close(); proc.wait(); print('ok',NF,'images')
