"""Interpolace vrcholu FFT: systematická chyba a rozptyl vůči šumu.

Profil: B 250 MHz, chirp 10 us, I/Q 4 MSPS (40 vzorků), Hannovo okno,
parabolická interpolace logaritmu amplitudy. Spuštění: python3 interpolace.py
"""
import cmath, math, random
c=3e8; B=250e6; T=10e-6; S=B/T; fs=4e6; N=40
dR=c/(2*B)
def r2f(R): return 2*R*S/c
def f2r(f): return f*c/(2*S)
win=[0.5-0.5*math.cos(2*math.pi*(n+0.5)/N) for n in range(N)]
def est(x,M,fguess):
    k0=round(fguess/fs*M)
    ks=range(k0-6,k0+7)
    mags={}
    for k in ks:
        s=0j
        w=cmath.exp(-2j*math.pi*k/M)
        z=1+0j
        for n in range(N):
            s+=x[n]*win[n]*z; z*=w
        mags[k]=abs(s)
    kmax=max(mags,key=mags.get)
    a,b,g=[20*math.log10(mags[k]+1e-30) for k in (kmax-1,kmax,kmax+1)]
    d=0.5*(a-g)/(a-2*b+g)
    return (kmax+d)*fs/M
random.seed(1)
for M in (64,128,256):
    worst=0
    for i in range(200):
        R=5+i*0.6/200*1.0  # posun pres jednu bunku
        f=r2f(R); x=[cmath.exp(2j*math.pi*f*n/fs) for n in range(N)]
        e=f2r(est(x,M,f))-R; worst=max(worst,abs(e))
    print(f"M={M}: max bias interpolace = {worst*100:.2f} cm ({worst/dR:.3f} bunky)")
# sum: SNR definovane jako N*A^2/sigma^2 (celkova energie / hustota sumu)
for snr_db in (20,30,40):
    snr=10**(snr_db/10); sig=math.sqrt(N/snr)  # A=1, sigma^2 per complex sample
    errs=[]
    for t in range(600):
        R=5+random.random()*0.6; f=r2f(R)
        x=[cmath.exp(2j*math.pi*f*n/fs+1j*0.3)+complex(random.gauss(0,sig/math.sqrt(2)),random.gauss(0,sig/math.sqrt(2))) for n in range(N)]
        errs.append(f2r(est(x,128,f))-R)
    m=sum(errs)/len(errs); sd=math.sqrt(sum((e-m)**2 for e in errs)/len(errs))
    crb=math.sqrt(6)/(2*math.pi)*dR/math.sqrt(snr)
    print(f"SNR {snr_db} dB: std {sd*100:.2f} cm | CRB {crb*100:.2f} cm | 0.707*dR/sqrt(SNR) {0.707*dR/math.sqrt(snr)*100:.2f} cm | pomer std/(dR/sqrt(SNR)) {sd/(dR/math.sqrt(snr)):.2f}")
