import sys; sys.path.insert(0,'.')
from nhd import *
OUT='/home/user/instagram-agent-skill/midia/aluguel-nx250-chique/'
CG='/tmp/claude-0/fonts/cg/package/files/cormorant-garamond-latin-'
_s={}
def serif(sz,w=600,it=False):
    k=(sz,w,it)
    if k not in _s: _s[k]=ImageFont.truetype(f"{CG}{w}-{'italic' if it else 'normal'}.woff2",sz)
    return _s[k]
_ot=ImageDraw.ImageDraw.text
def _tx(self,xy,text,fill=None,font=None,*a,**k):
    if font is not None and font in _s.values(): k.setdefault('features',['lnum'])
    return _ot(self,xy,text,fill,font,*a,**k)
ImageDraw.ImageDraw.text=_tx
IV=(244,239,230); IV2=(234,226,212); INK=(18,30,50); GLD=(170,132,78); GREY=(110,112,118)
W_,H_=1080,1350; M=80
def spaced(d,x,y,t,f,fill,sp=7,anchor='la'):
    ws=[d.textlength(c,font=f) for c in t]; tot=sum(ws)+sp*(len(t)-1); x0=x-tot/2 if anchor=='ma' else (x-tot if anchor=='ra' else x)
    for c,w in zip(t,ws): d.text((x0,y),c,font=f,fill=fill); x0+=w+sp
def frame(s,im,x,y,pad=14):
    d=ImageDraw.Draw(s); d.rectangle((x-pad,y-pad,x+im.width+pad-1,y+im.height+pad-1),outline=GLD,width=1); s.paste(im,(x,y))
def base(n=None):
    s=Image.new('RGB',(W_,H_),IV); d=ImageDraw.Draw(s)
    spaced(d,M,70,'COUNTRY NEGÓCIOS',sans(20,'sb'),INK,sp=6)
    if n: spaced(d,W_-M,70,f'{n:02d} — 06',sans(20,'m'),GREY,sp=3,anchor='ra')
    d.line((M,112,W_-M,112),fill=(214,204,186),width=1); return s,d
def foot(d,t='RESERVAS  ·  (44) 99884-6314'):
    d.line((M,H_-108,W_-M,H_-108),fill=(214,204,186),width=1); spaced(d,540,H_-78,t,sans(20,'sb'),INK,sp=5,anchor='ma')
def photo(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(P(n),w,h,cx=cx,cy=cy,zoom=zoom); a=np.array(im).astype(float); a=a*0.96+np.array([8,6,2]); return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def boat_on(s,w,x,y):
    b=boat(w); sh=Image.new('L',s.size,0); ImageDraw.Draw(sh).ellipse((x+w*0.08,y+b.height*0.82,x+w*0.95,y+b.height*0.98),fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(26)); s.paste((120,104,80),(0,0),sh); s.paste(b,(x,y),b)

def ph2(n,w,h,cx=0.5,cy=0.5,zoom=1.0): return photo(n,w,h,cx=cx,cy=cy,zoom=zoom)
# 01 capa
s=Image.new('RGB',(W_,H_),IV); d=ImageDraw.Draw(s)
spaced(d,540,90,'COUNTRY NEGÓCIOS',sans(22,'sb'),INK,sp=8,anchor='ma'); d.line((490,135,590,135),fill=GLD,width=1)
spaced(d,540,210,'ALUGUEL PARA FINS DE SEMANA',sans(24,'sb'),GLD,sp=7,anchor='ma')
d.text((540,255),'NX 250',font=serif(170,600),fill=INK,anchor='ma')
d.text((540,450),'Som de festa e espaço para a turma.',font=serif(48,500,True),fill=GREY,anchor='ma')
frame(s,ph2('1d5d97b3',920,540,cy=0.42),M,560)
for i,(a_,b_) in enumerate([('25','pés'),('10','pessoas'),('Som','de festa')]):
    cx=220+i*320; d.text((cx,1135),a_,font=serif(66,600),fill=INK,anchor='ma'); spaced(d,cx,1212,b_.upper(),sans(18,'sb'),GLD,sp=5,anchor='ma')
    if i: d.line((cx-160,1140,cx-160,1230),fill=(214,204,186),width=1)
foot(d); s.save(OUT+'01-capa.jpg',quality=97)
# 02 som
s,d=base(2); spaced(d,M,160,'A BORDO',sans(20,'sb'),GLD,sp=6)
d.text((M-4,190),'O som que',font=serif(80,600),fill=INK); d.text((M,280),'faz a festa.',font=serif(80,500,True),fill=INK)
frame(s,ph2('9667fb83',560,770,cx=0.6,cy=0.45),M,420)
s.paste(ph2('aafe8b4b',340,370,cy=0.4),(M+580,420)); s.paste(ph2('1d5d97b3',340,370,cx=0.78,cy=0.68,zoom=1.7),(M+580,820))
foot(d); s.save(OUT+'02-som.jpg',quality=97)
# 03 espaço
s,d=base(3); d.text((540,150),'Espaço para 10',font=serif(84,600),fill=INK,anchor='ma'); d.line((490,265,590,265),fill=GLD,width=1)
s.paste(ph2('3603af94',920,470,cy=0.27,zoom=1.15),(M,310))
s.paste(ph2('9667fb83',445,350,cx=0.45,cy=0.58),(M,805)); s.paste(ph2('aafe8b4b',445,350,cx=0.5,cy=0.4),(M+475,805))
d.text((540,1175),'Proa com sofá em U, cockpit amplo e popa com piso em EVA.',font=serif(34,500,True),fill=GREY,anchor='ma')
foot(d); s.save(OUT+'03-espaco.jpg',quality=97)
# 04 cockpit
s,d=base(4); frame(s,ph2('f6dce81e',560,820,cy=0.42),M,170)
x2=M+620; spaced(d,x2,190,'NO COMANDO',sans(20,'sb'),GLD,sp=6)
d.text((x2-3,225),'Cockpit',font=serif(80,600),fill=INK); d.text((x2,310),'completo',font=serif(72,500,True),fill=INK)
for k,t in enumerate(['Volante de madeira','Painel completo','Bancos em matelassê','Piso em EVA']):
    y=460+k*80; d.line((x2,y,x2+24,y),fill=GLD,width=2); d.text((x2+40,y-22),t,font=serif(34,500),fill=INK)
foot(d); s.save(OUT+'04-cockpit.jpg',quality=97)
# 05 ficha
s,d=base(5); d.text((540,150),'Ficha técnica',font=serif(84,600),fill=INK,anchor='ma'); d.line((490,265,590,265),fill=GLD,width=1)
s.paste(ph2('9667fb83',920,330,cx=0.5,cy=0.42,zoom=1.0),(M,310))
rows=[('Modelo','NX 250'),('Tipo','Proa aberta'),('Comprimento','25 pés · 7,5 m'),('Capacidade','10 pessoas'),('Som','Torre e subwoofer'),('Conforto','Toldo e sofá em U')]
y=700
for k_,v_ in rows:
    spaced(d,M,y+10,k_.upper(),sans(19,'sb'),GLD,sp=4); d.text((W_-M,y),v_,font=serif(42,500),fill=INK,anchor='ra'); y+=68; d.line((M,y-12,W_-M,y-12),fill=(214,204,186),width=1)
foot(d); s.save(OUT+'05-ficha.jpg',quality=97)
# 06 reserva
s=Image.new('RGB',(W_,H_),INK); d=ImageDraw.Draw(s)
spaced(d,540,90,'COUNTRY NEGÓCIOS',sans(22,'sb'),IV,sp=8,anchor='ma'); d.line((490,135,590,135),fill=GLD,width=1)
spaced(d,540,260,'AGENDA ABERTA',sans(24,'sb'),GLD,sp=8,anchor='ma')
d.text((540,310),'Reserve o seu',font=serif(110,600),fill=IV,anchor='ma'); d.text((540,440),'fim de semana',font=serif(104,500,True),fill=IV,anchor='ma')
for i,t in enumerate(['Sábados','Domingos','Feriados']):
    cx=230+i*310; d.rounded_rectangle((cx-130,640,cx+130,720),radius=40,outline=GLD,width=2); d.text((cx,680),t,font=serif(40,600),fill=IV,anchor='mm')
d.text((540,800),'NX 250 · até 10 pessoas · som de festa',font=serif(40,500,True),fill=(200,196,186),anchor='ma')
d.line((M,900,W_-M,900),fill=(60,74,96),width=1)
spaced(d,540,950,'RESERVAS PELO WHATSAPP',sans(22,'sb'),GLD,sp=6,anchor='ma')
d.text((540,995),'(44) 99884-6314',font=serif(96,600),fill=IV,anchor='ma')
d.text((540,1130),'ou comente NX',font=serif(40,500,True),fill=(200,196,186),anchor='ma')
L=logo(240); s.paste(L,(420,1220),L); s.save(OUT+'06-reserve.jpg',quality=97)
# STORY
st=Image.new('RGB',(1080,1920),IV); d=ImageDraw.Draw(st)
spaced(d,540,120,'COUNTRY NEGÓCIOS',sans(24,'sb'),INK,sp=8,anchor='ma'); d.line((490,170,590,170),fill=GLD,width=1)
spaced(d,540,280,'ALUGUEL PARA FINS DE SEMANA',sans(24,'sb'),GLD,sp=6,anchor='ma')
d.text((540,330),'NX 250',font=serif(190,600),fill=INK,anchor='ma')
d.text((540,560),'Até 10 pessoas · som de festa',font=serif(48,500,True),fill=GREY,anchor='ma')
frame(st,ph2('1d5d97b3',920,700,cy=0.42),80,680)
for i,(n_,cy_,lb) in enumerate([('3603af94',0.25,'Proa'),('f6dce81e',0.4,'Cockpit'),('aafe8b4b',0.35,'Som')]):
    x=80+i*317; st.paste(ph2(n_,286,250,cy=cy_),(x,1430)); d.text((x+143,1695),lb,font=serif(38,500,True),fill=INK,anchor='ma')
d.rectangle((140,1760,940,1850),fill=INK); spaced(d,540,1792,'RESERVE SEU FIM DE SEMANA',sans(24,'sb'),IV,sp=5,anchor='ma')
st.save(OUT+'story.jpg',quality=97)
names=['01-capa','02-som','03-espaco','04-cockpit','05-ficha','06-reserve']
ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story.jpg').resize((228,405))]
c=Image.new('RGB',(334*6+238,405),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width+10
c.save('/tmp/claude-0/nx_prev.jpg'); print('ok')
