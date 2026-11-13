from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import numpy as np, math
U='/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/'
OUT='/home/user/instagram-agent-skill/midia/2026-11-13-gti-2024/premium/'
NAVY=(21,39,61); DEEP=(9,18,31); GOLD=(196,152,90); GOLD2=(232,196,135); WHITE=(247,246,242); MUTE=(170,182,200)
F='/usr/share/fonts/opentype/inter/'
_fc={}
def f(w,s):
    k=(w,s)
    if k not in _fc: _fc[k]=ImageFont.truetype(F+{'black':'InterDisplay-Black.otf','xb':'InterDisplay-ExtraBold.otf','b':'InterDisplay-Bold.otf','m':'InterDisplay-Medium.otf','r':'InterDisplay-Medium.otf'}[w],s)
    return _fc[k]
# logo icon
sc=Image.open(U+'5bcece50-image.png').convert('RGB'); cx,cy,r=644,1261,424
ICON=sc.crop((cx-r,cy-r,cx+r,cy+r)); m=Image.new('L',(8*r,8*r),0); ImageDraw.Draw(m).ellipse((0,0,8*r-1,8*r-1),fill=255)
ICON.putalpha(m.resize((2*r,2*r),Image.LANCZOS))
def icon(s): return ICON.resize((s,s),Image.LANCZOS)
# jet cutout, fade stand
JET=Image.open('/tmp/claude-0/jet_final.png').convert('RGBA')
a=np.array(JET).astype(float); H=a.shape[0]
fade=np.clip((760-np.arange(H))/110,0,1)[:,None]; a[...,3]*=fade
JET=Image.fromarray(a.astype('uint8'),'RGBA').crop((0,0,800,760))
JET=ImageEnhance.Contrast(JET).enhance(1.08); JET=ImageEnhance.Color(JET).enhance(1.2)
JET=JET.filter(ImageFilter.UnsharpMask(2,70,2))
def jet(w):
    h=int(JET.height*w/JET.width); return JET.resize((w,h),Image.LANCZOS)
def studio(W,H,cy=None,glow=1.0):
    cy=cy if cy is not None else H*0.55
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    d=np.sqrt(((xx-W/2)/(W*0.75))**2+((yy-cy)/(H*0.6))**2)
    t=np.clip(d,0,1)[...,None]
    c1=np.array([38,68,105]); c0=np.array(DEEP)
    img=c1*(1-t)+c0*t
    # gold floor glow
    g=np.exp(-(((xx-W/2)/(W*0.42))**2+((yy-(cy+H*0.2))/(H*0.05))**2))[...,None]*glow
    img=img+g*np.array([120,85,40])*0.55
    return Image.fromarray(np.clip(img,0,255).astype('uint8'),'RGB')
def place_jet(bg,j,x,y,refl=True,shadow=True):
    if shadow:
        sh=Image.new('L',bg.size,0); d=ImageDraw.Draw(sh)
        d.ellipse((x+j.width*0.12,y+j.height*0.86,x+j.width*0.88,y+j.height*0.98),fill=170)
        sh=sh.filter(ImageFilter.GaussianBlur(28)); bg.paste((0,0,0),(0,0),sh)
    if refl:
        rf=j.transpose(Image.FLIP_TOP_BOTTOM); al=np.array(rf.split()[3]).astype(float)
        ramp=np.clip(1-np.arange(rf.height)/(rf.height*0.35),0,1)[:,None]*0.22
        rf.putalpha(Image.fromarray((al*ramp).astype('uint8')))
        rf=rf.filter(ImageFilter.GaussianBlur(3)); bg.paste(rf,(int(x),int(y+j.height*0.93)),rf)
    bg.paste(j,(int(x),int(y)),j)
def tw(d,t,font): return d.textlength(t,font=font)
def ctext(d,y,t,font,fill,W=1080,sp=0,cx=None):
    cx=cx if cx is not None else W/2
    if sp:
        ws=[d.textlength(c,font=font) for c in t]; T=sum(ws)+sp*(len(t)-1); x=cx-T/2
        for c,w in zip(t,ws): d.text((x,y),c,font=font,fill=fill); x+=w+sp
    else: d.text((cx-d.textlength(t,font=font)/2,y),t,font=font,fill=fill)
def pill(d,cx,y,t,font,bg,fg,padx=36,h=None,outline=None):
    w=d.textlength(t,font=font); b=d.textbbox((0,0),t,font=font); th=b[3]-b[1]; h=h or th+42
    d.rounded_rectangle((cx-w/2-padx,y,cx+w/2+padx,y+h),radius=h//2,fill=bg,outline=outline,width=3 if outline else 0)
    d.text((cx-w/2,y+(h-th)/2-b[1]),t,font=font,fill=fg); return h
def gold_text(W,H,x,y,t,font):
    """text filled with vertical gold gradient"""
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).text((x,y),t,font=font,fill=255)
    bb=m.getbbox() or (0,0,W,H); gy=np.clip((np.arange(H)-bb[1])/max(1,bb[3]-bb[1]),0,1)[:,None,None]
    g=np.array(GOLD2)*(1-gy)+np.array(GOLD)*gy
    g=np.repeat(g,W,1).astype('uint8'); return Image.fromarray(g,'RGB'),m
