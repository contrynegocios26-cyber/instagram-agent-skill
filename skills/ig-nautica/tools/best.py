import sys; sys.path.insert(0,'.')
from nhd import *
OUT='/home/user/instagram-agent-skill/midia/melhor-post/'
CG='/tmp/claude-0/fonts/cg/package/files/cormorant-garamond-latin-'
def serif(sz,w=600,it=False): return ImageFont.truetype(f"{CG}{w}-{'italic' if it else 'normal'}.woff2",sz)
NV=(22,39,60); NV3=(8,15,26); GD=(201,160,98); IV=(247,244,236)
LC=Image.open('/tmp/claude-0/logo_circle.png')
W_,H_=1080,1350
def grade(im):
    a=np.array(im).astype(float)/255
    a=0.5+(a-0.5)*1.12; a=np.clip(a,0,1)
    a=a**np.array([0.95,0.98,1.06])            # quente nas luzes
    lum=a.mean(-1,keepdims=True); a=lum+(a-lum)*0.92
    a=a*0.94+0.03
    h,w=a.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; v=1-0.42*(((xx-w/2)/(w*0.75))**2+((yy-h/2)/(h*0.75))**2); a*=np.clip(v,0.45,1)[...,None]
    return Image.fromarray((np.clip(a,0,1)*255).astype('uint8'))
def hero(n,cx=0.5,cy=0.5,zoom=1.0,w=W_,h=H_):
    im=Image.open(P(n)).convert('RGB'); iw,ih=im.size; r=w/h; ch=int(ih/zoom); cw=int(ch*r)
    if cw>iw: cw=iw; ch=int(cw/r)
    x0=int(min(max(iw*cx-cw/2,0),iw-cw)); y0=int(min(max(ih*cy-ch/2,0),ih-ch))
    im=im.crop((x0,y0,x0+cw,y0+ch)).resize((w,h),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,70,2))
    return grade(im)
def fade(im,top,bot,a1=235,a2=250,col=NV3):
    im=im.convert('RGBA'); w,h=im.size; ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top): d.line((0,y,w,y),fill=col+(int(a1*(1-y/top)**1.6),))
    for y in range(bot): d.line((0,h-1-y,w,h-1-y),fill=col+(int(a2*(1-y/bot)**0.75),))
    im.alpha_composite(ov); return im.convert('RGB')
def sp(d,x,y,t,f,fill,s=6,anchor='ma'):
    ws=[d.textlength(c,font=f) for c in t]; T=sum(ws)+s*(len(t)-1); x0=x-T/2 if anchor=='ma' else x
    for c,w in zip(t,ws): d.text((x0,y),c,font=f,fill=fill); x0+=w+s
def top_brand(s,d,y=56):
    c=LC.resize((92,92),Image.LANCZOS); s.paste(c,(W_//2-46,y),c); sp(d,540,y+110,'COUNTRY NEGÓCIOS',sans(20,'sb'),IV,s=8)
def button(d,y,t):
    f=sans(26,'b'); w=sum(d.textlength(c,font=f) for c in t)+5*(len(t)-1)
    d.rounded_rectangle((540-w/2-46,y,540+w/2+46,y+74),radius=37,fill=GD); sp(d,540,y+22,t,f,NV3,s=5)
def poster(n,cx,cy,zoom,kicker,l1,l2,specs,fn,top=480,bot=900):
    s=fade(hero(n,cx,cy,zoom),top,bot); d=ImageDraw.Draw(s); top_brand(s,d)
    sp(d,540,820,kicker,sans(22,'sb'),GD,s=7)
    d.text((540,860),l1,font=serif(96,600),fill=IV,anchor='ma',features=['lnum'])
    d.text((540,960),l2,font=serif(96,500,True),fill=IV,anchor='ma',features=['lnum'])
    d.line((500,1095,580,1095),fill=GD,width=2)
    d.text((540,1115),specs,font=serif(36,500,True),fill=(222,214,198),anchor='ma',features=['lnum'])
    button(d,1195,'RESERVE  ·  (44) 99884-6314')
    s.save(OUT+fn,quality=97); return s
# boat cutout showroom
BO=boat(1000)
def showroom(kicker,name,specs,fn):
    yy,xx=np.mgrid[0:H_,0:W_].astype(float)
    dd=np.sqrt(((xx-540)/700)**2+((yy-760)/620)**2); t=np.clip(dd,0,1)[...,None]
    bg=np.array([40,64,96])*(1-t)+np.array(NV3)*t
    floor=np.exp(-(((xx-540)/520)**2+((yy-930)/40)**2))[...,None]; bg=bg+floor*np.array([201,160,98])*0.35
    s=Image.fromarray(np.clip(bg,0,255).astype('uint8')); d=ImageDraw.Draw(s); top_brand(s,d)
    sp(d,540,250,kicker,sans(22,'sb'),GD,s=7)
    d.text((540,290),name,font=serif(190,600),fill=IV,anchor='ma',features=['lnum'])
    b=BO; sh=Image.new('L',s.size,0); ImageDraw.Draw(sh).ellipse((140,880,1000,960),fill=200); sh=sh.filter(ImageFilter.GaussianBlur(28)); s.paste((0,0,0),(0,0),sh)
    rf=b.transpose(Image.FLIP_TOP_BOTTOM); ra=np.array(rf).astype(float); ra[...,3]*=np.clip(1-np.arange(rf.height)/(rf.height*0.35),0,1)[:,None]*0.22; rf=Image.fromarray(ra.astype('uint8'),'RGBA')
    s.paste(rf,(W_-1000+20,560+b.height-30),rf); s.paste(b,(W_-1000+20,560),b); d=ImageDraw.Draw(s)
    d.text((540,1060),specs,font=serif(40,500,True),fill=(222,214,198),anchor='ma',features=['lnum'])
    button(d,1160,'RESERVE  ·  (44) 99884-6314')
    s.save(OUT+fn,quality=97); return s
a=poster('6c842673',0.5,0.5,1.0,'ALUGUEL · NHD 280','Seu fim de semana','no Rio Paraná.','Cabine climatizada · churrasqueira · 28 pés','nhd280-1-editorial.jpg')
b=showroom('ALUGUEL PARA FINS DE SEMANA','NHD 280','Cabine climatizada · churrasqueira · 280 hp','nhd280-2-showroom.jpg')
c=poster('1d5d97b3',0.5,0.5,1.0,'ALUGUEL · NX 250','Som, sol e','a sua turma.','Até 10 pessoas · torre de som · 25 pés','nx250-1-editorial.jpg')
e=poster('3603af94',0.5,0.32,1.15,'ALUGUEL · NX 250','Seu sábado','começa aqui.','Até 10 pessoas · proa aberta · som de festa','nx250-2-proa.jpg')
cv=Image.new('RGB',(432*4+30,540),'white')
for i,im in enumerate([a,b,c,e]): cv.paste(im.resize((432,540)),(i*442,0))
cv.save('/tmp/claude-0/best_prev.jpg'); print('ok')
