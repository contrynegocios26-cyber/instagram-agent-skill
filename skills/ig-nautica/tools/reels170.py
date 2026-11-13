import sys; sys.path.insert(0,'.')
from motor import *
import kit
OUT='/home/user/instagram-agent-skill/midia/2026-11-13-gti170-2025/'
SJ=Image.open('/tmp/claude-0/j170_studio.png')
def sj(w): return SJ.resize((w,int(SJ.height*w/SJ.width)),Image.LANCZOS)
BG=kit.studio(W,H,cy=1050); DARK=Image.new('RGB',(W,H),NAVY2)
PP=Image.open('/tmp/claude-0/p170_portrait.jpg').resize((1620,2880),Image.LANCZOS)
def view(cx,cy,z):
    w=W/z; h=H/z; cx=min(max(cx,w/2),W-w/2); cy=min(max(cy,h/2),H-h/2)
    return PP.crop(tuple(int(v*1.5) for v in (cx-w/2,cy-h/2,cx+w/2,cy+h/2))).resize((W,H),Image.BILINEAR)
def ti(t,font,fill):
    d=ImageDraw.Draw(Image.new('L',(1,1))); b=d.textbbox((0,0),t,font=font)
    im=Image.new('RGBA',(b[2]-b[0]+20,b[3]-b[1]+20),(0,0,0,0)); ImageDraw.Draw(im).text((10-b[0],10-b[1]),t,font=font,fill=fill); return im
def pc(bg,im,cx,cy,sc=1.0,al=1.0):
    if sc!=1: im=im.resize((max(1,int(im.width*sc)),max(1,int(im.height*sc))),Image.LANCZOS)
    if al<1: im=im.copy(); im.putalpha(im.split()[3].point(lambda v:int(v*al)))
    bg.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
LG=logo(320); TAGI=tag('110.000','modelo 2025',w=480,angle=0)
def jetframe(t,d,jy=760,w=900,z0=0.0):
    fr=BG.copy(); z=1+0.05*t/max(d,1); jw=int(w*z); j=sj(jw); kit.place_jet(fr,j,(W-jw)/2,jy); pc(fr,LG,W/2,150); return fr
def swing_tag(fr,t,x,y,w=None):
    ang=10*math.exp(-4*t)*math.cos(9*t); im=TAGI.rotate(6+ang,resample=Image.BICUBIC,expand=True)
    pc(fr,im,x,y-260*(1-eo(seg(t,0,0.5))))
def endcard(t,d):
    e=eo(seg(t,0,0.4)); fr=Image.new('RGB',(W,H),NAVY); dr=ImageDraw.Draw(fr)
    L=logo(700); fr.paste(L,(int(W/2-350),int(520-40*(1-e))),L)
    dr.text((W/2,860),'Seu verão começa aqui.',font=wide(58,850),fill=WHITE,anchor='mm'); dr.line((140,950,940,950),fill=GOLD,width=3)
    dr.text((W/2,1030),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((W/2,1110),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
    dr.text((W/2,1220),'ou comente EU QUERO',font=sans(40,'sb'),fill=GOLD,anchor='mm'); return fr
SPK_MODEL='Si Dú, gê tê i, cento e setenta'

# ===== REEL 1: 170 cavalos (estúdio) =====
T41=ti('41 HORAS',wide(120,900),TAG); T170=ti('170 CAVALOS',wide(108,900),WHITE)
def s1(t,d):
    fr=DARK.copy(); pc(fr,T41,W/2,760,sc=1+1.2*(1-eo(seg(t,0,0.3))),al=min(1,seg(t,0,0.2)*2))
    if t>0.9: pc(fr,T170,W/2,920,sc=1+1.2*(1-eo(seg(t,0.9,1.2))),al=min(1,seg(t,0.9,1.1)*2))
    return fr
def s2(t,d):
    fr=BG.copy(); r=eo(seg(t,0,0.9)); jw=int(900*(0.85+0.15*r)); j=sj(jw)
    if r<1: j=j.copy(); j.putalpha(j.split()[3].point(lambda v:int(v*min(1,r*1.4))))
    kit.place_jet(fr,j,(W-jw)/2,760+260*(1-r)); pc(fr,LG,W/2,150)
    pc(fr,ti('Sea-Doo GTI 170 · 2025',wide(52,850),TAG),W/2,330,al=seg(t,0.3,0.7)); return fr
def s3(t,d):
    fr=jetframe(t,d); c=int(170*eo(seg(t,0.1,1.4))); pc(fr,ti(f'{c} hp',wide(170,900),TAG),W/2,480)
    pc(fr,ti('Rotax 1630 ACE',sans(48,'sb'),WHITE),W/2,620,al=seg(t,0.3,0.6)); return fr
def s4(t,d):
    fr=jetframe(t+3,d+3); items=['Freio e ré iBR','Modos ECO e Sport','Regulador de velocidade']
    for k,it in enumerate(items):
        s=seg(t,0.2+k*0.6,0.5+k*0.6)
        if s>0:
            im=Image.new('RGBA',(820,110),(0,0,0,0)); dd=ImageDraw.Draw(im); dd.rounded_rectangle((0,0,819,109),radius=55,fill=(16,30,50),outline=TAG,width=3)
            dd.text((410,55),it,font=wide(40,850),fill=WHITE,anchor='mm'); pc(fr,im,W/2+80*(1-eo(s)),380+k*135,al=s)
    return fr
def s5(t,d):
    fr=BG.copy(); jw=900; j=sj(jw); kit.place_jet(fr,j,(W-jw)/2,520); pc(fr,LG,W/2,150)
    swing_tag(fr,t,W/2+40,1330); return fr
scenes=[dict(spk='Quarenta e uma horas. Cento e setenta cavalos.',cap=None,draw=s1,flash=False,min=2.6),
 dict(spk=f'{SPK_MODEL}, modelo dois mil e vinte e cinco.',cap='Sea-Doo GTI 170, modelo 2025.',draw=s2,ycap=1640),
 dict(spk='Motor Rotax de cento e setenta cavalos, o mais forte aspirado da Sea Dú.',cap='Motor Rotax de 170 cavalos, o mais forte aspirado da Sea-Doo.',draw=s3,ycap=1640),
 dict(spk='Freio e ré eletrônicos, modo econômico e regulador de velocidade.',cap='Freio e ré eletrônicos, modo econômico e regulador de velocidade.',draw=s4,ycap=1640),
 dict(spk='Cento e dez mil reais. Pagamento no cartão ou cheque.',cap='R$ 110 mil. Pagamento no cartão ou cheque.',draw=s5,ycap=1060),
 dict(spk='Comenta eu quero, ou chama a Cântri no zap!',cap='Comente EU QUERO ou chama a Country no zap!',draw=endcard,ycap=1450,min=3.0)]
print('R1',build(scenes,OUT+'reel-1-170-cavalos.mp4'))

# ===== REEL 2: equipado de fábrica (foto real) =====
PANEL_A=np.zeros((H,1))
for y in range(H): PANEL_A[y]=0 if y<1180 else min(1,((y-1180)/240)**1.3)
PM=Image.fromarray((np.repeat(PANEL_A,W,1)*255).astype('uint8')); PN=Image.new('RGB',(W,H),NAVY)
TOPG=Image.new('RGBA',(W,360),(0,0,0,0)); td=ImageDraw.Draw(TOPG)
for y in range(360): td.line((0,y,W,y),fill=NAVY+(int(190*(1-y/360)),))
def photoscene(v0,v1,l1,l2,small=False):
    def f(t,d):
        q=eio(seg(t,0,d)); fr=view(*[v0[j]+(v1[j]-v0[j])*q for j in range(3)])
        fr.paste(PN,(0,0),PM); fr.paste(TOPG,(0,0),TOPG); fr.paste(LG,(int(W/2-LG.width/2),90),LG)
        dr=ImageDraw.Draw(fr); s=eo(seg(t,0,0.35)); dx=int(-60*(1-s))
        if small: dr.text((72+dx,1350),l1,font=sans(46,'sb'),fill=GOLD); dr.text((68+dx,1405),l2,font=wide(96,850),fill=WHITE)
        else: dr.text((68+dx,1340),l1,font=wide(74,850),fill=WHITE); dr.text((68+dx,1435),l2,font=wide(74,850),fill=TAG)
        dr.line((72,1580,1008,1580),fill=GOLD,width=3); info_cols(dr,1600,[('Ano','2025'),('Horas de uso','41'),('Potência','170 hp')]); return fr
    return f
def pricescene(t,d):
    fr=photoscene((540,960,1.0),(540,940,1.05),'Sea-Doo','GTI 170',True)(t,d); ang=10*math.exp(-4*t)*math.cos(9*t)
    im=TAGI.rotate(6+ang,resample=Image.BICUBIC,expand=True); pc(fr,im,760,1150-260*(1-eo(seg(t,0,0.5)))); return fr
scenes=[dict(spk='Olha o que vem de fábrica nesse jet.',cap='Olha o que vem de fábrica nesse jet.',draw=photoscene((540,900,1.25),(540,960,1.05),'Olha o que','vem de fábrica'),flash=False),
 dict(spk='Freio e ré eletrônicos. Você para e manobra fácil na rampa.',cap='Freio e ré eletrônicos. Você para e manobra fácil na rampa.',draw=photoscene((640,560,1.7),(600,600,1.5),'Freio e ré','eletrônicos iBR')),
 dict(spk='Acelerador inteligente, com modo econômico e modo esporte.',cap='Acelerador inteligente, com modo econômico e modo esporte.',draw=photoscene((560,640,1.5),(540,700,1.35),'Modos ECO','e Sport')),
 dict(spk='Trim no guidão e regulador de velocidade.',cap='Trim no guidão e regulador de velocidade.',draw=photoscene((420,1050,1.45),(470,1000,1.3),'Trim VTS e','piloto de velocidade')),
 dict(spk='Três lugares, escada de embarque e só quarenta e uma horas.',cap='Três lugares, escada de embarque e só 41 horas.',draw=photoscene((700,800,1.4),(640,860,1.2),'Só 41 horas','de uso')),
 dict(spk='Cento e dez mil. Chama no zap!',cap='R$ 110 mil. Chama no zap!',draw=pricescene),
 dict(spk='Cântri Negócios.',cap=None,draw=endcard,min=2.6)]
print('R2',build(scenes,OUT+'reel-2-equipado.mp4',ycap=1010))

# ===== REEL 3: dor — antes de comprar jet usado =====
def card(n,title,sub,v0,v1):
    def f(t,d):
        q=eio(seg(t,0,d)); fr=view(*[v0[j]+(v1[j]-v0[j])*q for j in range(3)])
        fr.paste(PN,(0,0),PM); fr.paste(TOPG,(0,0),TOPG); fr.paste(LG,(int(W/2-LG.width/2),90),LG); dr=ImageDraw.Draw(fr)
        s=eob(seg(t,0,0.35)); pc(fr,ti(n,wide(150,900),TAG),150,1430,sc=0.6+0.4*s)
        dr.text((280,1350),title,font=wide(64,850),fill=WHITE); dr.text((282,1440),sub,font=sans(40,'sb'),fill=MUTE); return fr
    return f
HK1=ti('NÃO COMPRE',wide(96,900),WHITE); HK2=ti('JET SKI USADO',wide(96,900),TAG); HK3=ti('antes de ver isso',sans(60,'sb'),WHITE)
def hook(t,d):
    fr=view(540,960-40*t,1.1+0.05*t); ov=Image.new('RGBA',(W,H),NAVY2+(170,)); fr.paste(ov,(0,0),ov)
    pc(fr,HK1,W/2,760,sc=1+0.8*(1-eo(seg(t,0,0.25)))); 
    if t>0.35: pc(fr,HK2,W/2,880,sc=1+0.8*(1-eo(seg(t,0.35,0.6))))
    if t>0.8: pc(fr,HK3,W/2,1000,al=seg(t,0.8,1.0))
    pc(fr,LG,W/2,150); return fr
scenes=[dict(spk='Não compre jet ski usado antes de ver isso.',cap=None,draw=hook,flash=False),
 dict(spk='Um: horas de motor. Quanto menos, melhor. Esse aqui tem só quarenta e uma.',cap='Um: horas de motor. Quanto menos, melhor. Esse aqui tem só 41.',draw=card('1','Horas de motor','Esse tem só 41 h',(640,560,1.7),(600,600,1.5)),ycap=1000),
 dict(spk='Dois: o ano. Modelo dois mil e vinte e cinco, tecnologia atual.',cap='Dois: o ano. Modelo 2025, tecnologia atual.',draw=card('2','Ano do modelo','2025, linha atual',(420,1050,1.45),(470,1000,1.3)),ycap=1000),
 dict(spk='Três: veja de perto e confira a documentação antes de pagar.',cap='Três: veja de perto e confira a documentação antes de pagar.',draw=card('3','Veja de perto','e confira os documentos',(700,800,1.4),(640,860,1.2)),ycap=1000),
 dict(spk=f'Esse {SPK_MODEL} está aqui na Cântri, por cento e dez mil.',cap='Esse Sea-Doo GTI 170 está aqui na Country, por R$ 110 mil.',draw=pricescene,ycap=1010),
 dict(spk='Chama no zap e vem ver de perto!',cap='Chama no zap e vem ver de perto!',draw=endcard,ycap=1450,min=2.8)]
print('R3',build(scenes,OUT+'reel-3-antes-de-comprar.mp4',ycap=1010))
