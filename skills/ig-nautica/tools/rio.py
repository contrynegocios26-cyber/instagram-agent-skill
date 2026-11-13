# Cenário de rio ao pôr do sol (estilo Rio Paraná) + jet na água
import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
rng=np.random.default_rng(7)
def noise1d(n,scale,oct=4,seed=0):
    r=np.random.default_rng(seed); out=np.zeros(n)
    for o in range(oct):
        k=max(2,int(n/scale*2**o)); pts=r.random(k+1); x=np.linspace(0,k,n); out+=np.interp(x,np.arange(k+1),pts)/(2**o)
    return out/out.max()
def scene(W,H,horizon=0.52,sun_x=0.62,sun_y=None,t=0.0):
    hy=int(H*horizon); sun_y=sun_y if sun_y is not None else hy-int(H*0.06)
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    # céu
    s=np.clip(yy/hy,0,1)[...,None]
    top=np.array([28,34,72.]); mid=np.array([196,96,92.]); low=np.array([255,178,98.])
    sky=np.where(s<0.6, top*(1-s/0.6)+mid*(s/0.6), mid*(1-(s-0.6)/0.4)+low*((s-0.6)/0.4))
    sx=W*sun_x; d=np.sqrt((xx-sx)**2+((yy-sun_y)*1.1)**2)
    glow=np.exp(-d/(W*0.22))[...,None]; sky=sky+glow*np.array([255,190,110])*0.55
    core=np.clip(1-(d-W*0.045)/6,0,1)[...,None]; sky=sky*(1-core)+np.array([255,236,190])*core
    img=sky.copy()
    # nuvens finas
    for k in range(5):
        cy=hy*(0.18+0.13*k); band=np.exp(-((yy-cy)/(H*0.012))**2)*(0.5+0.5*np.sin(xx/W*6+k*1.7))
        img+=band[...,None]*np.array([255,150,120])*0.18
    # mata/ilhas no horizonte
    prof=noise1d(W,W/9,5,3); prof2=noise1d(W,W/5,4,9)
    fine=noise1d(W,W/60,4,21)
    treeh=(H*0.016+H*0.022*prof2+H*0.012*fine); island=(prof2>0.3)|(xx[0]<W*0.4)
    treeh=np.where(island,treeh,H*0.004)
    top_t=hy-treeh
    trees=(yy>=top_t[None,:])&(yy<hy)
    tc=np.array([34,40,46.])+np.array([60,30,10.])*glow*0.6
    img=np.where(trees[...,None],tc*(0.9+0.1*rng.random((H,W,1))),img)
    # água
    w=yy>=hy; depth=np.clip((yy-hy)/(H-hy),0,1)[...,None]
    water=np.array([60,52,78.])*(1-depth)+np.array([14,22,40.])*depth
    # reflexo do céu
    refl=np.flipud(sky[:hy])[:H-hy] if H-hy<=hy else None
    nz=np.random.default_rng(11).random((max(4,H//3),max(4,W//40)))
    nz=np.roll(nz,int(t*20),axis=1)
    rip=np.array(Image.fromarray((nz*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
    if refl is not None:
        rr=np.zeros_like(img); rr[hy:]=refl
        water=water*0.55+rr*0.45*(1-depth*0.7)
    # coluna de brilho do sol
    col=np.exp(-((xx-sx)/(W*(0.035+0.12*depth[...,0])))**2)*np.clip((rip-0.45)*3,0,1)
    water=water+col[...,None]*np.array([255,205,140])*(0.85-0.5*depth)
    water=water*(0.92+0.08*rip[...,None])
    img=np.where(w[...,None],water,img)
    # faixa clara na linha d'água
    img+=np.exp(-((yy-hy)/2.5)**2)[...,None]*np.array([255,200,150])*0.35
    return Image.fromarray(np.clip(img,0,255).astype('uint8')),hy
def grade(J):
    a=np.array(J).astype(float); h=a.shape[0]
    a[...,:3]*=np.array([1.0,0.9,0.86])*0.88
    g=np.clip(1-np.arange(h)/(h*0.5),0,1)[:,None,None]
    a[...,:3]+=g*np.array([70,38,10])*0.6
    return Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGBA')
def jet_in_water(bg,J,x,y,wl=0.82,t=0.0,foam=True):
    """J: RGBA jet; wl: fração da altura onde fica a linha d'água"""
    W,H=bg.size; jw,jh=J.size; cut=int(jh*wl)
    J=grade(J)
    top=J.crop((0,0,jw,cut))
    # reflexo
    rf=J.crop((0,0,jw,cut)).transpose(Image.FLIP_TOP_BOTTOM)
    a=np.array(rf).astype(float); ramp=np.clip(1-np.arange(rf.height)/(rf.height*0.5),0,1)[:,None]*0.35
    a[...,3]*=ramp; a[...,:3]*=0.7
    rf=Image.fromarray(a.astype('uint8'),'RGBA')
    # ondula o reflexo
    ra=np.array(rf); out=np.zeros_like(ra)
    for row in range(ra.shape[0]):
        sh=int(6*math.sin(row*0.25+t*6)); out[row]=np.roll(ra[row],sh,axis=0)
    rf=Image.fromarray(out,'RGBA').filter(ImageFilter.GaussianBlur(1.5))
    bg.paste(rf,(int(x),int(y+cut)),rf)
    # sombra escura na água logo abaixo
    sh=Image.new('L',bg.size,0); ImageDraw.Draw(sh).ellipse((x+jw*0.08,y+cut-14,x+jw*0.92,y+cut+26),fill=140); sh=sh.filter(ImageFilter.GaussianBlur(14))
    bg.paste((10,14,24),(0,0),sh)
    # jet: fade suave na linha d'água
    ta=np.array(top).astype(float); f=np.clip((cut-np.arange(cut))/10,0,1)[:,None]; ta[...,3]*=f
    bg.paste(Image.fromarray(ta.astype('uint8'),'RGBA'),(int(x),int(y)),Image.fromarray(ta.astype('uint8'),'RGBA'))
    if foam:
        # espuma: alpha = linha d'água do casco
        al=np.array(J.split()[3])[cut-1]>40; xs=np.where(al)[0]
        if len(xs):
            x0,x1=xs.min(),xs.max(); fm=Image.new('RGBA',bg.size,(0,0,0,0)); fd=ImageDraw.Draw(fm)
            r=np.random.default_rng(int(t*30)+1)
            fd.ellipse((x+x0-10,y+cut-10,x+x1+10,y+cut+16),fill=(255,250,245,150))
            band=fm.filter(ImageFilter.GaussianBlur(7)); fm=band; fd=ImageDraw.Draw(fm)
            for i in range(260):
                px=x+x0+r.random()*(x1-x0); py=y+cut+r.normal(0,4)
                rad=r.random()*3+1; fd.ellipse((px-rad,py-rad,px+rad,py+rad),fill=(255,255,255,int(80+r.random()*100)))
            for i in range(120):
                px=x+x0-r.random()*jw*0.45; py=y+cut+2+r.normal(0,3)
                rad=r.random()*3+1; fd.ellipse((px-rad*2,py-rad*0.6,px+rad*2,py+rad*0.6),fill=(255,255,255,int(40+r.random()*80)))
            fm=fm.filter(ImageFilter.GaussianBlur(1.2)); bg.alpha_composite(fm) if bg.mode=='RGBA' else bg.paste(fm,(0,0),fm)
    return bg
if __name__=='__main__':
    bg,hy=scene(1080,1350,horizon=0.5)
    bg.save('/tmp/claude-0/rio_scene.jpg',quality=92)
    J=Image.open('/tmp/claude-0/cut230_25.png'); J=J.crop(J.getbbox()); jw=860; J=J.resize((jw,int(J.height*jw/J.width)),Image.LANCZOS)
    jw=780; J=J.resize((jw,int(J.height*jw/J.width)),Image.LANCZOS) if False else J
    jet_in_water(bg,J,1080-jw+20,int(1350*0.80)-int(J.height*0.78),wl=0.78)
    bg.save('/tmp/claude-0/rio_test.jpg',quality=92)
