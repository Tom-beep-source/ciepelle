# Musique originale de défilé (composée par code, libre de droits) + design sonore
import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, json, os
# calé sur le montage : tempo, poses de talon et instants clés lus dans ../montage/timeline.json s'il existe
TL=json.load(open('../montage/timeline.json')) if os.path.exists('../montage/timeline.json') else {}
SR=48000; BPM=TL.get('bpm',120); BEAT=60/BPM; DUR=TL.get('dur',16.0); N=int(SR*DUR)
FADE0=TL.get('fade_start',10.8); CUT=TL.get('cut',13.25); HIT=TL.get('impact',13.45)
rng=np.random.default_rng(7)
def env_exp(n,tau): return np.exp(-np.arange(n)/(tau*SR))
def place(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if i<len(buf): buf[i:j]+=g*sig[:j-i]
def lp(x,fc,o=4): b,a=ss.butter(o,fc/(SR/2),'low'); return ss.lfilter(b,a,x)
def hp(x,fc,o=4): b,a=ss.butter(o,fc/(SR/2),'high'); return ss.lfilter(b,a,x)
def bp(x,f1,f2,o=2): b,a=ss.butter(o,[f1/(SR/2),f2/(SR/2)],'band'); return ss.lfilter(b,a,x)
# --- instruments
def kick():
    n=int(.45*SR); t=np.arange(n)/SR
    f=48+95*np.exp(-t/0.035); ph=2*np.pi*np.cumsum(f)/SR
    k=np.sin(ph)*env_exp(n,.16); k[:200]+=hp(rng.standard_normal(200),2000)*np.linspace(.5,0,200)
    return np.tanh(1.6*k)
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); x=hp(rng.standard_normal(n),7000)*env_exp(n,.06 if open_ else .012)
    return .35*x
def clap():
    n=int(.25*SR); x=bp(rng.standard_normal(n),900,3500)
    e=np.zeros(n)
    for d in (0,.009,.019,.03): e+=np.exp(-np.clip(np.arange(n)/SR-d,0,None)/.012)*(np.arange(n)/SR>=d)
    return .5*x*e*env_exp(n,.09)
def saw(f,n,det=0.0):
    t=np.arange(n)/SR; return 2*((t*f*(1+det))%1)-1
def bass(f,dur):
    n=int(dur*SR); x=.6*np.sin(2*np.pi*f*np.arange(n)/SR)+.4*lp(saw(f,n),420)
    e=np.minimum(1,np.arange(n)/(.004*SR))*env_exp(n,.18); return np.tanh(1.3*x*e)
def stab(freqs,dur):
    n=int(dur*SR); x=sum(saw(f,n,d) for f in freqs for d in (-.004,.004))/(2*len(freqs))
    x=lp(x,1400); e=np.minimum(1,np.arange(n)/(.006*SR))*env_exp(n,.22); return x*e
K,HC,HO,CL=kick(),hat(),hat(True),clap()
drums=np.zeros(N); bas=np.zeros(N); stb=np.zeros(N)
bars=int(np.ceil(CUT/(4*BEAT)))
prog=[55.0,55.0,49.0,52.0]  # A, A, G, Ab... -> sombre
chords=[[220,261.6,329.6,392],[220,261.6,329.6,392],[196,246.9,293.7,349.2],[207.7,246.9,311.1,370]]
for b in range(bars):
    t0=b*4*BEAT
    for q in range(4):
        tq=t0+q*BEAT
        if tq>=CUT: break
        place(drums,K,tq,.95)
        # version dynamique : charleston en doubles croches dès la 1re mesure, clap dès la 2e
        place(drums,HC,tq+BEAT/2,.8); place(drums,HC,tq+BEAT*0.25,.3); place(drums,HC,tq+BEAT*0.75,.4)
        if b>=1 and q in (1,3): place(drums,CL,tq,.7)
        if q==3: place(drums,HO,tq+BEAT/2,.5)
        place(bas,bass(prog[b%4],BEAT*.45),tq+BEAT/2,.8)
    if t0+3.5*BEAT<CUT: place(stb,stab(chords[b%4],BEAT*1.2),t0+2.5*BEAT,.55)
mix=.9*drums+.75*bas+.6*stb
# --- talons (clic + corps) sur le temps pour l'animatique
def heel():
    n=int(.12*SR); x=bp(rng.standard_normal(n),1800,6000)*env_exp(n,.008)*1.2
    x+= .5*np.sin(2*np.pi*180*np.arange(n)/SR)*env_exp(n,.02); return x
def snowstep():
    n=int(.22*SR); x=lp(bp(rng.standard_normal(n),250,2500)*(rng.random(n)<.35),1800)*env_exp(n,.05); return 1.4*x
heels=np.zeros(N); snows=np.zeros(N)
for h in TL.get('heels',[.12+i*BEAT for i in range(int(13.2/BEAT))]):
    place(heels,heel(),h,.55*(1+.08*rng.standard_normal()))
for h in TL.get('snow_steps',[]):
    place(snows,snowstep(),h,.5)
# --- réverbération de grande salle (réponse impulsionnelle synthétique stéréo)
def ir(rt=2.6,pre=.028):
    n=int(rt*1.2*SR); t=np.arange(n)/SR
    out=[]
    for ch in range(2):
        x=rng.standard_normal(n)*np.exp(-6.9*t/rt); x=lp(x,6500,2)
        early=np.zeros(n)
        for d,g in [(.011,.6),(.019,.45),(.027,.4),(.041,.3),(.053,.25),(.071,.2)]:
            early[int((d+.003*ch)*SR)]+=g
        x=np.concatenate([np.zeros(int(pre*SR)),x])[:n]+early
        out.append(x/np.max(np.abs(x)))
    return np.array(out)
IR=ir()
def reverb(x): return np.array([ss.fftconvolve(x,IR[c])[:N] for c in range(2)])*.12
dry=np.vstack([mix,mix])+np.vstack([heels*1.0,heels*0.9])
wet=reverb(mix*.6+heels*1.4)
# --- "le son s'éloigne": 10.8s -> 13.25s, la salle se referme: passe-bas progressif, plus d'écho, volume en baisse
t=np.arange(N)/SR
a=np.clip((t-FADE0)/(CUT-FADE0),0,1)
full=dry+wet*(.55+1.6*a)            # l'écho monte quand on s'éloigne
v=[full]+[np.array([lp(full[c],fc,2) for c in range(2)]) for fc in (2600,900,320)]
w=np.vstack([np.clip(1-3*a,0,1),
             np.clip(1-np.abs(3*a-1),0,1),
             np.clip(1-np.abs(3*a-2),0,1),
             np.clip(3*a-2,0,1)])
out=sum(v[i]*w[i] for i in range(4))
out*=10**(-20*a**1.3/20)            # -20 dB à la fin
out[:,t>=CUT]=0                    # coupure nette avant le logo
# vent d'hiver et pas dans la neige : dehors, donc ni écho ni filtre de salle ; ils s'arrêtent avec la coupure
wind=lp(rng.standard_normal(N),700,2)*(.5+.5*np.sin(2*np.pi*.35*t+1.3))**2
wa=np.clip((t-TL.get('outside',CUT))/.6,0,1)*(t<CUT)*.35
out+=np.vstack([wind*wa+snows,wind*wa*.9+snows*.9])
# --- impact du logo (13.45 s): sub-boom + craquement + longue queue de réverbe
def impact():
    n=int(2.5*SR); tt=np.arange(n)/SR
    sub=np.sin(2*np.pi*(38+30*np.exp(-tt/.08))*tt)*np.exp(-tt/.9)
    crack=bp(rng.standard_normal(n),200,5000)*np.exp(-tt/.05)
    return np.tanh(1.8*(.9*sub+.6*crack))
imp=np.zeros(N); place(imp,impact(),HIT,1.0)
out+=np.vstack([imp,imp])*.32+reverb(imp)*.9
# whoosh inverse juste avant l'impact
n=int(.5*SR); w=hp(rng.standard_normal(n),1500)*np.linspace(0,1,n)**3*.25
wb=np.zeros(N); place(wb,w,HIT-.5); out+=np.vstack([wb,wb*.8])
# fondu final + normalisation
out[:,t>DUR-.7]*=np.linspace(1,0,(t>DUR-.7).sum())
out=out/np.max(np.abs(out))*0.89
wf.write('bande-son-defile.wav',SR,(out.T*32767).astype(np.int16))
print('ok', out.shape)
