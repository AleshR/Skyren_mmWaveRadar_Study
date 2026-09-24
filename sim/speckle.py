"""Speckle na drsné zdi: Monte Carlo s gaussovským svazkem a náhodnými fázemi.

Vyřazuje 10 % nejslabších měření (hluboké útlumy). Spuštění: python3 speckle.py [počet běhů]
"""
import cmath, math, random, sys
c=3e8; B=250e6; T=10e-6; S=B/T; fs=4e6; N=40; M=128
f0=24.125e9; lam=c/f0
win=[0.5-0.5*math.cos(2*math.pi*(n+0.5)/N) for n in range(N)]
def est(x,fguess):
    k0=round(fguess/fs*M); mags={}
    for k in range(k0-6,k0+7):
        s=0j; w=cmath.exp(-2j*math.pi*k/M); z=1+0j
        for n in range(N): s+=x[n]*win[n]*z; z*=w
        mags[k]=abs(s)
    kmax=max(mags,key=mags.get)
    a,b,g=[20*math.log10(mags[k]+1e-30) for k in (kmax-1,kmax,kmax+1)]
    return (kmax+0.5*(a-g)/(a-2*b+g))*fs/M, mags[kmax]
def run(R, hpbw_deg, tilt_deg, trials, nsc=1200, seed=2):
    random.seed(seed)
    th3=math.radians(hpbw_deg); a2=8*math.log(2)/th3**2   # dvoucestny vykon exp(-a2*th^2)
    tl=math.radians(tilt_deg)
    Rb=R  # vzdalenost v ose
    res=[]
    for t in range(trials):
        x=[0j]*N
        for i in range(nsc):
            # smer v kuzelu do 2.2*HPBW
            thx=random.uniform(-1.1,1.1)*th3*2; thy=random.uniform(-1.1,1.1)*th3*2
            th2=thx*thx+thy*thy
            # rovina: normala sklonena o tl v ose x; vzdalenost podel smeru (thx,thy)
            # jednotkovy smer d=(sin thx, sin thy, ~cos); normala n=(sin tl,0,cos tl); rovina n.p = Rb*cos tl
            dx,dy=math.tan(thx),math.tan(thy); dz=1.0
            nrm=math.sqrt(dx*dx+dy*dy+1); dx/=nrm; dy/=nrm; dz/=nrm
            denom=dx*math.sin(tl)+dz*math.cos(tl)
            Ri=Rb*math.cos(tl)/denom
            amp=math.exp(-0.5*a2*th2)          # amplituda ~ sqrt(dvoucestneho vykonu)
            ph=random.uniform(0,2*math.pi)     # drsnost -> nahodna faze
            fb=2*Ri*S/c
            ph0=ph+4*math.pi*Ri/lam
            z=cmath.exp(1j*ph0)*amp; w=cmath.exp(2j*math.pi*fb/fs)
            for n in range(N): x[n]+=z; z*=w
        f,mag=est(x,2*Rb*S/c)
        res.append((f*c/(2*S)-Rb, mag))
    return res
def stats(res, gate=0.0):
    mags=sorted(m for _,m in res); thr=mags[int(gate*len(mags))] if gate>0 else -1
    e=[r for r,m in res if m>=thr]
    m=sum(e)/len(e); sd=math.sqrt(sum((v-m)**2 for v in e)/len(e))
    e2=sorted(e); med=e2[len(e2)//2]
    return m,sd,med,len(e)

if __name__ == "__main__":
    # Drsná zeď ve 5 m: posun od stopy svazku a kolísání jednoho měření (speckle).
    # Model: b = R*sg^2*(1+tan^2 a), s_R = R*sg*sqrt(sg^2+tan^2 a), sg = HPBW/sqrt(16 ln 2)
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    R = 5.0
    print("HPBW naklon | posun sim/model [cm] | kolisani sim/model [cm]")
    for hp, tl in ((22, 0), (22, 15), (14, 0), (14, 15), (10, 0), (10, 15)):
        res = run(R, hp, tl, trials=trials, seed=7)
        sg = math.radians(hp) / math.sqrt(16 * math.log(2)); ta = math.tan(math.radians(tl))
        b = R * sg**2 * (1 + ta**2); sR = R * sg * math.sqrt(sg**2 + ta**2)
        m, sd, med, n = stats(res, 0.1)
        print(f"{hp:3d} {tl:3d} | {m*100:5.2f} / {b*100:5.2f} | {sd*100:5.2f} / {sR*100:5.2f}")
