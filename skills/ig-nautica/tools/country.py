# Layout padrão Country Negócios
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, math
U='/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/'
OUT='/home/user/instagram-agent-skill/midia/2026-11-13-gti-2024/country/'
NAVY=(22,38,60); NAVY2=(14,27,45); GOLD=(190,148,88); TAG=(216,190,140); WHITE=(247,246,242); MUTE=(176,186,202)
ARCH='/tmp/claude-0/fonts/package/files/archivo-latin-wdth-normal.woff2'
INTER='/usr/share/fonts/opentype/inter/'
_c={}
def wide(size,wght=800,wdth=125):
    k=('w',size,wght,wdth)
    if k not in _c:
        f=ImageFont.truetype(ARCH,size); f.set_variation_by_axes([wght,wdth]); _c[k]=f
    return _c[k]
def sans(size,w='m'):
    k=('s',size,w)
    if k not in _c: _c[k]=ImageFont.truetype(INTER+{'r':'Inter-Regular.otf','m':'Inter-Medium.otf','sb':'Inter-SemiBold.otf','b':'Inter-Bold.otf'}[w],size)
    return _c[k]
LOGO=Image.open('/tmp/claude-0/logo_white.png')
def logo(w): return LOGO.resize((w,int(LOGO.height*w/LOGO.width)),Image.LANCZOS)
JETF=Image.open('/tmp/claude-0/jet_final.png')
def photo_portrait():
    p=Image.open('/tmp/claude-0/photo_clean.jpg').convert('RGB')
    bg=p.filter(ImageFilter.GaussianBlur(16)); bg=ImageEnhance.Brightness(bg).enhance(0.9)
    j=JETF; bg.paste(j,(31,264),j)
    bg=ImageEnhance.Contrast(bg).enhance(1.1); bg=ImageEnhance.Color(bg).enhance(1.22); bg=bg.filter(ImageFilter.UnsharpMask(2,60,2))
    return bg  # 900x1600
def fade_to_navy(im,y0,y1,col=NAVY):
    W,H=im.size; m=np.zeros((H,1))
    for y in range(H): m[y]=0 if y<y0 else (1 if y>y1 else ((y-y0)/(y1-y0))**1.3)
    mask=Image.fromarray((np.repeat(m,W,1)*255).astype('uint8')); im.paste(col,(0,0),mask)
def tag(price,sub,w=420,angle=6,small='R$'):
    h=int(w*0.6); S=3
    im=Image.new('RGBA',(w*S,h*S),(0,0,0,0)); d=ImageDraw.Draw(im)
    n=int(h*S*0.28)
    d.polygon([(n,0),(w*S,0),(w*S,h*S),(0,h*S),(0,n)],fill=TAG)
    cx,cy=int(w*S*0.38),int(h*S*0.17); r=int(14*S)
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=NAVY); d.ellipse((cx-r+8,cy-r+8,cx+r-8,cy+r-8),fill=(40,52,70))
    d.text((int(30*S/1),int(h*S*0.33)),small,font=sans(26*S,'b'),fill=NAVY)
    d.text((int(26*S),int(h*S*0.45)),price,font=wide(int(w*0.165)*S,900),fill=NAVY)
    if sub: d.text((int(30*S),int(h*S*0.78)),sub,font=sans(23*S,'sb'),fill=NAVY)
    im=im.resize((w,h),Image.LANCZOS)
    pad=Image.new('RGBA',(w+200,h+200),(0,0,0,0))
    # string
    sd=ImageDraw.Draw(pad); hx,hy=100+int(w*0.38),100+int(h*0.17)
    pts=[(hx+ (w*0.9)*t, hy-90*math.sin(math.pi*t*0.9)+ 40*t*t) for t in np.linspace(0,1,40)]
    sd.line(pts,fill=GOLD,width=5)
    sh=Image.new('RGBA',pad.size,(0,0,0,0)); shm=Image.new('L',pad.size,0); shm.paste(im.split()[3],(108,112)); shm=shm.filter(ImageFilter.GaussianBlur(10))
    pad.paste((0,0,0),(0,0),shm.point(lambda v:int(v*0.45)))
    pad.paste(im,(100,100),im)
    # redraw string end through hole on top
    sd=ImageDraw.Draw(pad); sd.line(pts[:6],fill=GOLD,width=5)
    return pad.rotate(angle,resample=Image.BICUBIC,expand=True)
def info_cols(d,y,cols,x0=72,x1=1008):
    cw=(x1-x0)/len(cols)
    for i,(k,v) in enumerate(cols):
        x=x0+i*cw; d.text((x,y),k,font=sans(28,'sb'),fill=GOLD); d.text((x,y+38),v,font=wide(40,800),fill=WHITE)
def footer(im,d,y,W=1080,phone='(44) 99884-6314'):
    L=logo(250); im.paste(L,(72,y),L)
    t1='Chame no WhatsApp'; t2=phone
    d.text((W-72-d.textlength(t1,font=sans(26,'m')),y+4),t1,font=sans(26,'m'),fill=WHITE)
    d.text((W-72-d.textlength(t2,font=wide(34,800)),y+40),t2,font=wide(34,800),fill=WHITE)
