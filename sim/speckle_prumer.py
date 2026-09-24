"""Průměrování speckle při přibližování: pevná drsná zeď, radar se přiblíží o 1,2 m
(20 měření po 6 cm, tj. 4 kHz při 240 m/s). Spuštění: python3 speckle_prumer.py [počet běhů]
"""
import cmath, math, random, sys
c=3e8; B=250e6; T=10e-6; S=B/T; fs=4e6; N=40; M=128; lam=c/24.125e9
win=[0.5-0.5*math.cos(2*math.pi*(n+0.5)/N) for n in range(N)]
def est(x,fguess):
    k0=round(fguess/fs*M); mags={}
    for k in range(k0-14,k0+15):
        s=0j; w=cmath.exp(-2j*math.pi*k/M); z=1+0j
        for n in range(N): s+=x[n]*win[n]*z; z*=w
        mags[k]=abs(s)
    kmax=max((k for k in mags if k-1 in mags and k+1 in mags),key=mags.get)
    a,b,g=[20*math.log10(mags[k]+1e-30) for k in (kmax-1,kmax,kmax+1)]
    return (kmax+0.5*(a-g)/(a-2*b+g))*fs/M, mags[kmax]
def trial(hp,tl,Rc=5.0,L=1.2,nmeas=20,nsc=600,seed=0):
    rnd=random.Random(seed)
    th3=math.radians(hp); a2=8*math.log(2)/th3**2; t=math.radians(tl)
    Rmax=Rc+L/2; ext=2.4*th3*Rmax
    e1=(math.cos(t),0,-math.sin(t)); e2=(0,1,0)
    sc=[(rnd.uniform(-ext,ext),rnd.uniform(-ext,ext),rnd.uniform(0,2*math.pi)) for _ in range(nsc)]
    sg=th3/math.sqrt(16*math.log(2)); b=lambda R: R*sg*sg*(1+math.tan(t)**2)
    errs=[]
    for k in range(nmeas):
        Rb=Rc+L/2-k*L/(nmeas-1)   # vzdalenost v ose
        x=[0j]*N
        for (u,v,ph) in sc:
            px=u*e1[0]; py=v; pz=Rb+u*e1[2]   # radar v pocatku, zed pres (0,0,Rb)
            Ri=math.sqrt(px*px+py*py+pz*pz)
            th2=math.atan2(math.hypot(px,py),pz)**2
            amp=math.exp(-0.5*a2*th2)
            if amp<1e-4: continue
            z=cmath.exp(1j*(ph+4*math.pi*Ri/lam))*amp; w=cmath.exp(2j*math.pi*(2*Ri*S/c)/fs)
            for n in range(N): x[n]+=z; z*=w
        f,mag=est(x,2*Rb*S/c)
        errs.append((f*c/(2*S)-Rb-b(Rb),mag))
    mags=sorted(m for _,m in errs); thr=mags[int(0.1*len(mags))]
    e=[r for r,m in errs if m>=thr]
    return sum(e)/len(e), errs
for hp,tl in ((22,0),(22,15)):
    means=[]; singles=[]
    for s in range(int(sys.argv[1])):
        m,errs=trial(hp,tl,seed=100+s); means.append(m); singles+= [r for r,_ in errs]
    mu=sum(means)/len(means); sd=math.sqrt(sum((v-mu)**2 for v in means)/len(means))
    sg=math.radians(hp)/math.sqrt(16*math.log(2)); ta=math.tan(math.radians(tl)); sR=5*sg*math.sqrt(sg*sg+ta*ta)
    print(f"HPBW {hp} tilt {tl}: std prumeru pres 1.2 m = {sd*100:.1f} cm (model {math.sqrt(sR*lam*5/(4*1.2))*100:.1f}), zbytkovy bias {mu*100:.1f} cm, n={len(means)}")
