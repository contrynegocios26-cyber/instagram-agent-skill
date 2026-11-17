import sys; sys.path.insert(0,'.')
from nhd import *
OUT='/home/user/instagram-agent-skill/midia/aluguel-nhd280-moderno/'
DK=(10,14,24); DK2=(22,28,42); LIME=(214,255,63); WH=(255,255,255); GR=(160,168,184)
W_,H_=1080,1350; M=64
def cond(sz,w=900): return wide(sz,w,62)
def pop(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(P(n),w,h,cx=cx,cy=cy,zoom=zoom); im=ImageEnhance.Contrast(im).enhance(1.12); im=ImageEnhance.Color(im).enhance(1.1); return im
def grad(im,top=0,bot=0,a1=200,a2=235,col=DK):
    im=im.convert('RGBA'); w,h=im.size; ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top): d.line((0,y,w,y),fill=col+(int(a1*(1-y/top)**1.4),))
    for y in range(bot): d.line((0,h-1-y,w,h-1-y),fill=col+(int(a2*(1-y/bot)**1.2),))
    im.alpha_composite(ov); return im.convert('RGB')
def pill(d,x,y,t,bg=LIME,fg=DK,f=None,anchor='l'):
    f=f or sans(26,'b'); w=d.textlength(t,font=f); h=56
    if anchor=='c': x=x-(w+44)/2
    d.rounded_rectangle((x,y,x+w+44,y+h),radius=28,fill=bg); d.text((x+22,y+h/2),t,font=f,fill=fg,anchor='lm'); return w+44
def opill(d,x,y,t,f=None):
    f=f or sans(26,'sb'); w=d.textlength(t,font=f); d.rounded_rectangle((x,y,x+w+44,y+56),radius=28,outline=WH,width=2); d.text((x+22,y+28),t,font=f,fill=WH,anchor='lm'); return w+44
def sticker(s,cx,cy,r,l1,l2,rot=-12):
    S=Image.new('RGBA',(2*r+20,2*r+20),(0,0,0,0)); d=ImageDraw.Draw(S)
    pts=[]; n=28
    for k in range(2*n):
        rr=r if k%2==0 else r*0.9; a=k*math.pi/n; pts.append((r+10+rr*math.cos(a),r+10+rr*math.sin(a)))
    d.polygon(pts,fill=LIME); d.text((r+10,r-8),l1,font=cond(int(r*0.62)),fill=DK,anchor='mm'); d.text((r+10,r+r*0.42),l2,font=sans(int(r*0.2),'b'),fill=DK,anchor='mm')
    S=S.rotate(rot,resample=Image.BICUBIC); s.paste(S,(int(cx-S.width/2),int(cy-S.height/2)),S)
def brand(s,d,dark=True,n=None):
    L=logo(200); s.paste(L,(M,50),L)
    if n: d.text((W_-M,74),f'{n}/6',font=sans(26,'b'),fill=WH,anchor='ra')
def cta_bar(d,y=H_-96):
    d.text((M,y),'RESERVAS  (44) 99884-6314',font=sans(28,'b'),fill=WH)

U2='/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/'
def Q(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(U2+n+'-image.jpg',w,h,cx=cx,cy=cy,zoom=zoom); im=ImageEnhance.Contrast(im).enhance(1.1); return ImageEnhance.Color(im).enhance(1.08)
def glow(w,h,cx,cy):
    yy,xx=np.mgrid[0:h,0:w].astype(float); d_=np.sqrt(((xx-cx)/(w*0.7))**2+((yy-cy)/(h*0.45))**2)
    t=np.clip(d_,0,1)[...,None]; a=np.array([34,46,70])*(1-t)+np.array(DK)*t; return Image.fromarray(a.astype('uint8'))
# 01 CAPA (lancha em estúdio escuro)
s=glow(W_,H_,540,760); d=ImageDraw.Draw(s); brand(s,d)
pill(d,M,170,'ALUGUEL · FIM DE SEMANA')
d.text((M-6,240),'NHD',font=cond(260),fill=WH); d.text((M+470,240),'280',font=cond(260),fill=LIME)
b=boat(1020); sh=Image.new('L',s.size,0); ImageDraw.Draw(sh).ellipse((140,1010,1040,1080),fill=170); sh=sh.filter(ImageFilter.GaussianBlur(30)); s.paste((0,0,0),(0,0),sh)
s.paste(b,(W_-1020+20,600),b); d=ImageDraw.Draw(s)
sticker(s,880,560,105,'A/C','CABINE',rot=12)
x=M
for t in ['28 pés','280 hp','Churrasqueira','Banheiro']: x+=opill(d,x,1130,t)+12
cta_bar(d); s.save(OUT+'01-capa.jpg',quality=97)
# 02 CHURRASCO
s=grad(Q('ca86e549',W_,H_,cy=0.62),top=820,bot=560,a1=255,a2=245); d=ImageDraw.Draw(s); brand(s,d,n=2)
d.text((M-4,150),'CHURRAS',font=cond(200),fill=LIME); d.text((M-4,345),'NO RIO.',font=cond(150),fill=WH)
x=M
for t in ['Churrasqueira','Tábua','Pia']: x+=pill(d,x,1060,t,bg=WH)+14
d.text((M,1150),'A carne assando e a galera na água.',font=sans(32,'sb'),fill=WH)
cta_bar(d); s.save(OUT+'02-churrasco.jpg',quality=97)
# 03 CABINE
s=grad(Q('a37e75d6',W_,H_,cy=0.55),top=820,bot=600,a1=255,a2=245); d=ImageDraw.Draw(s); brand(s,d,n=3)
d.text((M-4,150),'CABINE',font=cond(200),fill=WH); d.text((M-4,345),'GELADA.',font=cond(150),fill=LIME)
x=M
for t in ['Ar-condicionado','Banheiro com ducha','Mesa']: x+=pill(d,x,1040,t,bg=WH)+14
d.text((M,1130),'Pra descansar, trocar de roupa e fugir do sol.',font=sans(32,'sb'),fill=WH)
cta_bar(d); s.save(OUT+'03-cabine.jpg',quality=97)
# 04 BENTO
s=Image.new('RGB',(W_,H_),DK); d=ImageDraw.Draw(s); brand(s,d,n=4)
d.text((M,140),'TUDO A BORDO',font=cond(110),fill=WH)
g=16; X0=M; Y0=290; cw=(W_-2*M-g)//2
tile(s,Q('6c842673',cw,420,cy=0.5),X0,Y0,r=26)
d.rounded_rectangle((X0+cw+g,Y0,X0+2*cw+g,Y0+200),radius=26,fill=LIME); d.text((X0+cw+g+30,Y0+18),'28',font=cond(130),fill=DK); d.text((X0+cw+g+30,Y0+150),'PÉS · 8,4 M',font=sans(26,'b'),fill=DK)
d.rounded_rectangle((X0+cw+g,Y0+220,X0+2*cw+g,Y0+420),radius=26,fill=DK2); d.text((X0+cw+g+30,Y0+238),'280',font=cond(130),fill=WH); d.text((X0+cw+g+30,Y0+370),'HP DE MOTOR',font=sans(26,'b'),fill=LIME)
tile(s,Q('069e17aa',cw,520,cy=0.6),X0,Y0+440,r=26); tile(s,pop('819e42ac',cw,520,cy=0.42),X0+cw+g,Y0+440,r=26)
d=ImageDraw.Draw(s)
for (x,y,t) in [(X0+20,Y0+360,'Popa com sofá'),(X0+20,Y0+880,'Acabamento em teca'),(X0+cw+g+20,Y0+880,'Som potente')]: pill(d,x,y,t,bg=WH,f=sans(24,'b'))
cta_bar(d); s.save(OUT+'04-a-bordo.jpg',quality=97)
# 05 FICHA
s=Image.new('RGB',(W_,H_),DK); d=ImageDraw.Draw(s); brand(s,d,n=5)
d.text((M,140),'FICHA',font=cond(130),fill=WH); d.text((M+330,140),'NHD 280',font=cond(130),fill=LIME)
items=[('28','PÉS','8,4 m de comprimento'),('280','HP','motor de centro'),('A/C','CABINE','com mesa e banheiro'),('BBQ','CHURRASQUEIRA','com tábua e pia')]
for k,(a_,b_,c_) in enumerate(items):
    x=M+(k%2)*(cw+g); y=330+(k//2)*(340+g); hl=(k==1)
    d.rounded_rectangle((x,y,x+cw,y+340),radius=26,fill=LIME if hl else DK2)
    d.text((x+30,y+20),a_,font=cond(150),fill=DK if hl else WH); d.text((x+32,y+215),b_,font=sans(28,'b'),fill=DK if hl else LIME); d.text((x+32,y+262),c_,font=sans(26,'m'),fill=(40,48,20) if hl else GR)
tile(s,Q('80a5a056',W_-2*M,230,cy=0.3,zoom=1.0),M,1040,r=26); d=ImageDraw.Draw(s)
cta_bar(d,H_-80); s.save(OUT+'05-ficha.jpg',quality=97)
# 06 CTA
s=Image.new('RGB',(W_,H_),LIME); d=ImageDraw.Draw(s)
L=logo(220); a=np.array(L); a[...,:3]=np.where(a[...,3:4]>0,np.array(DK),a[...,:3]); La=Image.fromarray(a); s.paste(La,(M,56),La)
d.text((W_-M,80),'6/6',font=sans(26,'b'),fill=DK,anchor='ra')
d.text((M-6,190),'SEU FIM',font=cond(230),fill=DK); d.text((M-6,420),'DE SEMANA.',font=cond(180),fill=DK)
tile(s,Q('6c842673',W_-2*M,330,cy=0.5),M,690,r=30); d=ImageDraw.Draw(s)
d.text((M,1060),'Reserve seu sábado, domingo ou feriado.',font=sans(34,'b'),fill=DK)
d.rounded_rectangle((M,1130,W_-M,1250),radius=60,fill=DK); d.text((540,1190),'(44) 99884-6314',font=cond(76),fill=LIME,anchor='mm')
d.text((540,1290),'ou comente LANCHA',font=sans(28,'b'),fill=DK,anchor='mm')
s.save(OUT+'06-reserve.jpg',quality=97)
# STORY
st=glow(1080,1920,540,1000); d=ImageDraw.Draw(st); L=logo(240); st.paste(L,(420,110),L)
pill(d,540,260,'ALUGUEL · FIM DE SEMANA',anchor='c')
d.text((540,360),'NHD 280',font=cond(260),fill=WH,anchor='ma')
b=boat(1040); st.paste(b,(60,740),b); sticker(st,880,700,105,'A/C','CABINE',rot=12); d=ImageDraw.Draw(st)
for i,(n_,lb) in enumerate([('ca86e549','Churrasqueira'),('a37e75d6','Cabine'),('6c842673','Espaço')]):
    x=60+i*330; tile(st,Q(n_,300,300,cy=0.5),x,1180,r=22); d=ImageDraw.Draw(st); pill(d,x+150,1450,lb,bg=WH,f=sans(24,'b'),anchor='c')
d.rounded_rectangle((150,1600,930,1720),radius=60,fill=LIME); d.text((540,1660),'RESERVE AGORA',font=cond(72),fill=DK,anchor='mm')
d.text((540,1770),'[ cole o link do WhatsApp aqui ]',font=sans(26,'m'),fill=WH,anchor='ma')
st.save(OUT+'story.jpg',quality=97)
# FROTA (as duas lanchas)
s=Image.new('RGB',(W_,H_),DK); d=ImageDraw.Draw(s); L=logo(200); s.paste(L,(M,50),L)
pill(d,M,150,'ALUGUEL DE LANCHAS'); d.text((M-4,220),'ESCOLHA',font=cond(150),fill=WH); d.text((M+560,220),'A SUA.',font=cond(150),fill=LIME)
for i,(img,nm,l1,l2) in enumerate([(Q('6c842673',cw,560,cy=0.5),'NHD 280','Cabine com ar','Churrasqueira'),(Q('9debdc7d',cw,560,cy=0.45),'NX 250','Até 10 pessoas','Som de festa')]):
    x=M+i*(cw+g); tile(s,img,x,420,r=26); d=ImageDraw.Draw(s)
    d.rounded_rectangle((x,1000,x+cw,1190),radius=26,fill=LIME if i else DK2)
    fg=DK if i else WH
    d.text((x+28,1012),nm,font=cond(90),fill=fg); d.text((x+30,1120),f'{l1} · {l2}',font=sans(24,'b'),fill=DK if i else LIME)
d.text((M,H_-96),'RESERVAS  (44) 99884-6314',font=sans(28,'b'),fill=WH)
s.save('/home/user/instagram-agent-skill/midia/aluguel-nhd280-moderno/frota-escolha-a-sua.jpg',quality=97)
names=['01-capa','02-churrasco','03-cabine','04-a-bordo','05-ficha','06-reserve','frota-escolha-a-sua']
ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story.jpg').resize((228,405))]
c=Image.new('RGB',(334*7+238,405),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width+10
c.save('/tmp/claude-0/nhdpop_prev.jpg'); print('ok')
