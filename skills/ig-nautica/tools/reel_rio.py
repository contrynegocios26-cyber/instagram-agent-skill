import sys; sys.path.insert(0,'.')
from motor import *
import rio
OUT='/home/user/instagram-agent-skill/midia/layouts-teste/'
J=Image.open('/tmp/claude-0/cut230_25.png').convert('RGBA'); J=J.crop(J.getbbox())
JW=900; J=J.resize((JW,int(J.height*JW/J.width)),Image.LANCZOS)
cache={}
def bg(t):
    k=int(t*15)%45
    if k not in cache: cache[k]=rio.scene(W,H,horizon=0.5,sun_x=0.3,t=k/15)[0]
    return cache[k].copy()
LG=logo(320)
def ti(t,font,fill):
    d=ImageDraw.Draw(Image.new('L',(1,1))); b=d.textbbox((0,0),t,font=font)
    im=Image.new('RGBA',(b[2]-b[0]+30,b[3]-b[1]+30),(0,0,0,0)); ImageDraw.Draw(im).text((15-b[0],15-b[1]),t,font=font,fill=fill,stroke_width=5,stroke_fill=(12,18,32))
    if im.width>960: im=im.resize((960,int(im.height*960/im.width)),Image.LANCZOS)
    return im
def pc(b,im,cx,cy,al=1.0):
    if al<1: im=im.copy(); im.putalpha(im.split()[3].point(lambda v:int(v*al)))
    b.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
def place(fr,t,x):
    y=int(H*0.70)-int(J.height*0.78)+int(8*math.sin(t*2.2))
    rio.jet_in_water(fr,J,x,y,wl=0.78,t=t); return fr
def topchrome(fr):
    fr.paste(LG,(int(W/2-LG.width/2),90),LG); d=ImageDraw.Draw(fr); d.text((W-40,H-30),'imagem ilustrativa',font=sans(22,'m'),fill=(220,220,230),anchor='rs')
T1=ti('IMAGINA',wide(110,900),WHITE); T2=ti('SEU SÁBADO',wide(110,900),TAG)
def s1(t,d):
    fr=bg(t); pc(fr,T1,W/2,520,al=eo(seg(t,0,0.4))); pc(fr,T2,W/2,660,al=eo(seg(t,0.5,0.9))); topchrome(fr); return fr
TM=ti('Sea-Doo GTX 230',wide(84,900),WHITE); TY=ti('modelo 2025',sans(50,'sb'),TAG)
def s2(t,d):
    fr=bg(t+3); x=W-JW+20+int(700*(1-eo(seg(t,0,1.6)))); place(fr,t,x); pc(fr,TM,W/2,420,al=eo(seg(t,0.6,1.0))); pc(fr,TY,W/2,520,al=eo(seg(t,0.9,1.3))); topchrome(fr); return fr
TH=ti('17 HORAS',wide(110,900),TAG); TC=ti('230 CAVALOS',wide(90,900),WHITE)
def s3(t,d):
    fr=bg(t+6); place(fr,t+3,W-JW+20); pc(fr,TH,W/2,420,al=eo(seg(t,0,0.3))); pc(fr,TC,W/2,560,al=eo(seg(t,0.5,0.8))); topchrome(fr); return fr
def s4(t,d):
    fr=bg(t+9); place(fr,t+6,W-JW+20); topchrome(fr)
    x0,y0,x1,y1=60,330,1020,640; reg=fr.crop((x0,y0,x1,y1)).filter(ImageFilter.GaussianBlur(18)); fr.paste(reg,(x0,y0))
    ov=Image.new('RGBA',fr.size,(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle((x0,y0,x1,y1),radius=36,fill=NAVY2+(int(180*eo(seg(t,0,0.4))),)); fr.paste(ov,(0,0),ov)
    dr=ImageDraw.Draw(fr); a=eo(seg(t,0.1,0.5))
    if a>0:
        pc(fr,ti('R$ 145.000',wide(100,900),WHITE),W/2,440,al=a); pc(fr,ti('(44) 99884-6314',wide(56,850),TAG),W/2,560,al=a)
    return fr
def endcard(t,d):
    e=eo(seg(t,0,0.4)); fr=Image.new('RGB',(W,H),NAVY); dr=ImageDraw.Draw(fr)
    L=logo(700); fr.paste(L,(int(W/2-350),int(520-40*(1-e))),L)
    dr.text((W/2,860),'Seu verão começa aqui.',font=wide(58,850),fill=WHITE,anchor='mm'); dr.line((140,950,940,950),fill=GOLD,width=3)
    dr.text((W/2,1030),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((W/2,1110),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
    dr.text((W/2,1220),'ou comente EU QUERO',font=sans(40,'sb'),fill=GOLD,anchor='mm'); return fr
sc=[dict(spk='Imagina seu sábado no rio Paraná...',cap=None,draw=s1,flash=False,min=2.4),
 dict(spk='com um Si Dú, gê tê xis, duzentos e trinta, modelo dois mil e vinte e cinco.',cap='com um Sea-Doo GTX 230, modelo 2025.',draw=s2,flash=False,ycap=1560,min=3.2),
 dict(spk='Só dezessete horas de uso, e duzentos e trinta cavalos.',cap='Só 17 horas de uso, e 230 cavalos.',draw=s3,flash=False,ycap=1560),
 dict(spk='Cento e quarenta e cinco mil, aqui na Cântri. Chama no zap!',cap='R$ 145 mil, aqui na Country. Chama no zap!',draw=s4,flash=False,ycap=1560),
 dict(spk='Cântri Negócios.',cap=None,draw=endcard,min=2.6)]
print(build(sc,OUT+'reel-rio-parana-gtx230.mp4'))
