import sys; sys.path.insert(0,'.')
from nhd import *
OUT='/home/user/instagram-agent-skill/midia/aluguel-nhd280-chique/'
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
    if n: spaced(d,W_-M,70,f'{n:02d} — 07',sans(20,'m'),GREY,sp=3,anchor='ra')
    d.line((M,112,W_-M,112),fill=(214,204,186),width=1); return s,d
def foot(d,t='RESERVAS  ·  (44) 99884-6314'):
    d.line((M,H_-108,W_-M,H_-108),fill=(214,204,186),width=1); spaced(d,540,H_-78,t,sans(20,'sb'),INK,sp=5,anchor='ma')
def photo(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(P(n),w,h,cx=cx,cy=cy,zoom=zoom); a=np.array(im).astype(float); a=a*0.96+np.array([8,6,2]); return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def boat_on(s,w,x,y):
    b=boat(w); sh=Image.new('L',s.size,0); ImageDraw.Draw(sh).ellipse((x+w*0.08,y+b.height*0.82,x+w*0.95,y+b.height*0.98),fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(26)); s.paste((120,104,80),(0,0),sh); s.paste(b,(x,y),b)
# 01 capa
s=Image.new('RGB',(W_,H_),IV); d=ImageDraw.Draw(s)
L=logo(230); Ld=Image.new('RGBA',L.size,INK+(0,)); 
spaced(d,540,90,'COUNTRY NEGÓCIOS',sans(22,'sb'),INK,sp=8,anchor='ma'); d.line((490,135,590,135),fill=GLD,width=1)
spaced(d,540,250,'ALUGUEL PARA FINS DE SEMANA',sans(24,'sb'),GLD,sp=7,anchor='ma')
d.text((540,300),'NHD 280',font=serif(190,600),fill=INK,anchor='ma')
d.text((540,520),'O seu fim de semana a bordo.',font=serif(54,500,True),fill=GREY,anchor='ma')
boat_on(s,980,W_-980,640)
for i,(a_,b_) in enumerate([('28','pés'),('280','hp'),('Ar','na cabine')]):
    cx=220+i*320; d.text((cx,1105),a_,font=serif(70,600),fill=INK,anchor='ma'); spaced(d,cx,1190,b_.upper(),sans(18,'sb'),GLD,sp=5,anchor='ma')
    if i: d.line((cx-160,1110,cx-160,1210),fill=(214,204,186),width=1)
foot(d); s.save(OUT+'01-capa.jpg',quality=97)
# 02 editorial churrasco
s,d=base(2); im=photo('bb2369bb',920,760,cy=0.55); frame(s,im,M,170)
spaced(d,M,975,'A BORDO',sans(20,'sb'),GLD,sp=6); d.text((M-4,1005),'Churrasco com vista',font=serif(76,600),fill=INK); d.text((M,1095),'para o Rio Paraná.',font=serif(76,500,True),fill=INK)
foot(d); s.save(OUT+'02-churrasco.jpg',quality=97)
# 03 comodidades
s,d=base(3); d.text((540,150),'Comodidades',font=serif(84,600),fill=INK,anchor='ma'); d.line((490,265,590,265),fill=GLD,width=1)
cells=[('bb2369bb',0.55,'Churrasqueira'),('ee557b53',0.5,'Cabine'),('494e31cb',0.45,'Ar-condicionado'),('550c4289',0.5,'Banheiro'),('819e42ac',0.42,'Som'),('06f7f0bf',0.42,'Solário de popa')]
cw,ch_=(W_-2*M-60)//3,250
for k,(n_,cy_,lb) in enumerate(cells):
    x=M+(k%3)*(cw+30); y=310+(k//3)*(ch_+110); s.paste(photo(n_,cw,ch_,cy=cy_),(x,y)); d.text((x+cw/2,y+ch_+22),lb,font=serif(38,500,True),fill=INK,anchor='ma')
d.text((540,1110),'Tudo pronto para receber a sua família e os seus amigos.',font=serif(36,500,True),fill=GREY,anchor='ma')
foot(d); s.save(OUT+'03-comodidades.jpg',quality=97)
# 04 cabine
s,d=base(4); frame(s,photo('ee557b53',560,820,cy=0.45),M,170)
x2=M+620; spaced(d,x2,190,'INTERIOR',sans(20,'sb'),GLD,sp=6)
d.text((x2-3,225),'Cabine',font=serif(78,600),fill=INK); d.text((x2,310),'climatizada',font=serif(70,500,True),fill=INK)
for k,t in enumerate(['Ar-condicionado','Mesa de madeira','Banheiro com ducha','Acabamento em teca']):
    y=460+k*80; d.line((x2,y,x2+24,y),fill=GLD,width=2); d.text((x2+40,y-22),t,font=serif(36,500),fill=INK)
s.paste(photo('494e31cb',300,300,cy=0.45),(x2,800))
foot(d); s.save(OUT+'04-cabine.jpg',quality=97)
# 05 detalhes
s,d=base(5); d.text((540,150),'Detalhes',font=serif(84,600),fill=INK,anchor='ma'); d.line((490,265,590,265),fill=GLD,width=1)
s.paste(photo('0dcbd92a',920,430,cy=0.30,zoom=1.5),(M,310))
s.paste(photo('819e42ac',445,380,cy=0.42),(M,770)); s.paste(photo('280e20c2',445,380,cy=0.6),(M+475,770))
foot(d); s.save(OUT+'05-detalhes.jpg',quality=97)
# 06 ficha
s,d=base(6); d.text((540,150),'Ficha técnica',font=serif(84,600),fill=INK,anchor='ma'); d.line((490,265,590,265),fill=GLD,width=1)
boat_on(s,780,W_-780,290)
rows=[('Modelo','NHD 280'),('Comprimento','28 pés · 8,4 m'),('Motor','280 hp'),('Cabine','Mesa e ar-condicionado'),('Banheiro','Pia e ducha'),('Lazer','Churrasqueira, som e toldo'),('Banho','Plataforma com escada')]
y=700
for k_,v_ in rows:
    spaced(d,M,y+10,k_.upper(),sans(19,'sb'),GLD,sp=4); d.text((W_-M,y),v_,font=serif(40,500),fill=INK,anchor='ra'); y+=62; d.line((M,y-10,W_-M,y-10),fill=(214,204,186),width=1)
foot(d); s.save(OUT+'06-ficha.jpg',quality=97)
# 07 reserva (escuro, contraste)
s=Image.new('RGB',(W_,H_),INK); d=ImageDraw.Draw(s)
spaced(d,540,90,'COUNTRY NEGÓCIOS',sans(22,'sb'),IV,sp=8,anchor='ma'); d.line((490,135,590,135),fill=GLD,width=1)
spaced(d,540,260,'AGENDA ABERTA',sans(24,'sb'),GLD,sp=8,anchor='ma')
d.text((540,310),'Reserve o seu',font=serif(110,600),fill=IV,anchor='ma'); d.text((540,440),'fim de semana',font=serif(104,500,True),fill=IV,anchor='ma')
for i,t in enumerate(['Sábados','Domingos','Feriados']):
    cx=230+i*310; d.rounded_rectangle((cx-130,640,cx+130,720),radius=40,outline=GLD,width=2); d.text((cx,680),t,font=serif(40,600),fill=IV,anchor='mm')
d.text((540,800),'As datas do verão são as primeiras a acabar.',font=serif(40,500,True),fill=(200,196,186),anchor='ma')
d.line((M,900,W_-M,900),fill=(60,74,96),width=1)
spaced(d,540,950,'RESERVAS PELO WHATSAPP',sans(22,'sb'),GLD,sp=6,anchor='ma')
d.text((540,995),'(44) 99884-6314',font=serif(96,600),fill=IV,anchor='ma')
d.text((540,1130),'ou comente LANCHA',font=serif(40,500,True),fill=(200,196,186),anchor='ma')
L=logo(240); s.paste(L,(420,1220),L); s.save(OUT+'07-reserve.jpg',quality=97)
# STORY
st=Image.new('RGB',(1080,1920),IV); d=ImageDraw.Draw(st)
spaced(d,540,120,'COUNTRY NEGÓCIOS',sans(24,'sb'),INK,sp=8,anchor='ma'); d.line((490,170,590,170),fill=GLD,width=1)
spaced(d,540,300,'ALUGUEL PARA FINS DE SEMANA',sans(24,'sb'),GLD,sp=6,anchor='ma')
d.text((540,350),'NHD 280',font=serif(200,600),fill=INK,anchor='ma')
boat_on(st,1000,80,640)
for i,(n_,lb) in enumerate([('bb2369bb','Churrasqueira'),('ee557b53','Cabine'),('819e42ac','Som')]):
    x=80+i*317; st.paste(photo(n_,286,286,cy=0.5),(x,1130)); d.text((x+143,1440),lb,font=serif(40,500,True),fill=INK,anchor='ma')
d.rectangle((140,1600,940,1700),fill=INK); spaced(d,540,1636,'RESERVE SEU FIM DE SEMANA',sans(24,'sb'),IV,sp=5,anchor='ma')
d.text((540,1760),'[ cole o link do WhatsApp aqui ]',font=sans(24,'m'),fill=GREY,anchor='ma')
st.save(OUT+'story.jpg',quality=97)
names=['01-capa','02-churrasco','03-comodidades','04-cabine','05-detalhes','06-ficha','07-reserve']
ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story.jpg').resize((228,405))]
c=Image.new('RGB',(334*7+238,405),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width+10
c.save('/tmp/claude-0/chic_prev.jpg'); print('ok')
