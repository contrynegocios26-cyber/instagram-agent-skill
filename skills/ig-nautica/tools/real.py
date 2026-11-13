# Composição realista do jet em foto real do rio
import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
SR='/tmp/claude-0/aen/sr/'
def bg_crop(name,W,H,cx_frac=0.5,cy_frac=0.5,zoom=1.0):
    im=Image.open(SR+name).convert('RGB'); iw,ih=im.size
    r=W/H; ch=int(ih/zoom); cw=int(ch*r)
    if cw>iw: cw=iw; ch=int(cw/r)
    x0=int(min(max(iw*cx_frac-cw/2,0),iw-cw)); y0=int(min(max(ih*cy_frac-ch/2,0),ih-ch))
    return im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
def match(J,tint=(0.97,1.0,1.07),bright=1.1,contrast=1.12,sat=1.05):
    a=np.array(J).astype(float); rgb=a[...,:3]
    rgb*=np.array(tint)*bright; m=rgb.mean(); rgb=(rgb-m)*contrast+m
    h,w=rgb.shape[:2]; yy,xx=np.mgrid[0:h,0:w]
    hl=np.clip(1-(yy/h)*1.6,0,1)*np.clip(1-xx/w*0.6,0,1); rgb+=hl[...,None]*np.array([22,22,18])
    a[...,:3]=np.clip(rgb,0,255); out=Image.fromarray(a.astype('uint8'),'RGBA')
    return ImageEnhance.Color(out).enhance(sat)
def grain(J,s=3.0,seed=0):
    a=np.array(J).astype(float); n=np.random.default_rng(seed).normal(0,s,a.shape[:2])[...,None]; a[...,:3]=np.clip(a[...,:3]+n,0,255)
    return Image.fromarray(a.astype('uint8'),'RGBA')
def place(bg,J,x,y,wl=0.8,t=0.0,seed=1):
    """cola o jet com linha d'água realista. (x,y)=canto sup-esq do jet; wl=fração da altura na linha d'água"""
    W,H=bg.size; J=grain(match(J),seed=seed); jw,jh=J.size; cut=int(jh*wl)
    rng=np.random.default_rng(seed+int(t*30))
    # 1) escurecer água ao redor/baixo do casco (sombra)
    sh=Image.new('L',bg.size,0); d=ImageDraw.Draw(sh); d.ellipse((x+jw*0.02,y+cut-jh*0.03,x+jw*1.0,y+cut+jh*0.07),fill=150)
    sh=sh.filter(ImageFilter.GaussianBlur(jw*0.03)); bg.paste((22,40,44),(0,0),sh)
    # 2) reflexo distorcido
    al=np.array(J.split()[3]); top=J.crop((0,0,jw,cut))
    rf=top.transpose(Image.FLIP_TOP_BOTTOM); ra=np.array(rf).astype(float)
    ramp=np.clip(1-np.arange(rf.height)/(rf.height*0.4),0,1)[:,None]*0.33; ra[...,3]*=ramp; ra[...,:3]=ra[...,:3]*0.55+np.array([30,48,50])*0.45
    out=np.zeros_like(ra)
    for r_ in range(ra.shape[0]): out[r_]=np.roll(ra[r_],int(7*math.sin(r_*0.3+t*5)),axis=0)
    rf=Image.fromarray(out.astype('uint8'),'RGBA').filter(ImageFilter.GaussianBlur(2)); bg.paste(rf,(int(x),int(y+cut)),rf)
    # 3) jet: acima da linha = normal; abaixo = casco submerso esverdeado sumindo
    a=np.array(J).astype(float); yy=np.arange(jh)[:,None]
    xr=np.arange(jw); wave=cut+4*np.sin(xr/22.0+t*6)+2.5*np.sin(xr/8.0+t*9)+rng.normal(0,0.8,jw)
    below=yy-wave[None,:]
    sub=np.clip(1-below/26.0,0,1)*0.55          # parte submersa visível
    above=(below<=0).astype(float)
    edge=np.clip(1-np.abs(below)/2.0,0,1)
    water=np.array([70,108,104.])
    rgb=a[...,:3].copy()
    mix=np.clip(below/10.0,0,1)[...,None]*(below>0)[...,None]
    rgb=rgb*(1-mix*0.75)+water*mix*0.75
    alpha=a[...,3]*np.maximum(above,sub*(below>0))
    a[...,:3]=rgb; a[...,3]=alpha
    Jc=Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGBA')
    bg.paste(Jc,(int(x),int(y)),Jc)
    # 4) faixa clara irregular + onda de proa + gotas
    row=np.array(J.split()[3])[min(cut,jh-1)]>40; xs=np.where(row)[0]
    if len(xs):
        x0,x1=xs.min(),xs.max(); fm=Image.new('L',bg.size,0); fd=ImageDraw.Draw(fm)
        for px in range(x0,x1,3):
            th=2+3*abs(math.sin(px/31.0+t*3))+2*rng.random(); py=y+wave[px]
            fd.ellipse((x+px-4,py-th*0.6,x+px+4,py+th),fill=int(110+60*rng.random()))
        # onda de proa (lado direito do jet = proa)
        bx=x+x1; by=y+wave[min(x1,jw-1)]
        for k in range(28):
            ang=rng.uniform(-0.15,0.5); L=rng.uniform(15,70)
            ex=bx-L*0.2*math.cos(ang)+rng.uniform(-10,20); ey=by+L*0.35*math.sin(ang)+rng.uniform(-4,6)
            fd.line((bx-rng.uniform(0,30),by+rng.uniform(-3,3),ex,ey),fill=int(70+70*rng.random()),width=int(rng.uniform(2,5)))
        # esteira atrás (popa à esquerda)
        sx_=x+x0; sy_=y+wave[x0]
        for k in range(40):
            L=rng.uniform(20,140); fd.line((sx_,sy_+rng.uniform(-2,4),sx_-L,sy_+rng.uniform(0,10)+L*0.04),fill=int(40+50*rng.random()),width=int(rng.uniform(2,4)))
        fm=fm.filter(ImageFilter.GaussianBlur(2.2))
        bg.paste((236,242,240),(0,0),fm)
        dr=Image.new('RGBA',bg.size,(0,0,0,0)); dd=ImageDraw.Draw(dr)
        for k in range(50):
            px=bx+rng.normal(-10,18); py=by-abs(rng.normal(0,14)); r_=rng.uniform(0.8,2.2)
            dd.ellipse((px-r_,py-r_,px+r_,py+r_),fill=(245,250,250,int(120+100*rng.random())))
        bg.paste(dr,(0,0),dr)
    return bg
