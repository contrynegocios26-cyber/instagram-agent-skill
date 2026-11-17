import sys; sys.path.insert(0,'.')
from nhd import *
OUT='/home/user/instagram-agent-skill/midia/aluguel-nx250-country/'
DK=(22,39,60); DK2=(34,56,86); LIME=(196,152,90); WH=(247,246,242); GR=(176,186,202)
LC=Image.open('/tmp/claude-0/logo_circle.png')
def lc(sz): return LC.resize((sz,sz),Image.LANCZOS)
W_,H_=1080,1350; M=64
def cond(sz,w=900): return wide(sz,w,62)
def pop(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(P(n),w,h,cx=cx,cy=cy,zoom=zoom); im=ImageEnhance.Contrast(im).enhance(1.12); im=ImageEnhance.Color(im).enhance(1.1); return im
def grad(im,top=0,bot=0,a1=200,a2=235,col=(9,17,29)):
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
    c=lc(96); s.paste(c,(M,40),c); d.text((M+116,62),'COUNTRY',font=wide(30,900),fill=WH); d.text((M+118,100),'N E G Ó C I O S',font=sans(16,'sb'),fill=LIME)
    if n: d.text((W_-M,74),f'{n}/6',font=sans(26,'b'),fill=WH,anchor='ra')
def cta_bar(d,y=H_-96):
    d.text((M,y),'RESERVAS  (44) 99884-6314',font=sans(28,'b'),fill=WH)
# 01 CAPA
s=grad(pop('1d5d97b3',W_,H_,cy=0.45),top=360,bot=700,a1=210,a2=245); d=ImageDraw.Draw(s); brand(s,d)
pill(d,M,700,'ALUGUEL · FIM DE SEMANA')
d.text((M-6,770),'NX 250',font=cond(270),fill=WH)
d.text((M,1060),'Som alto, galera junta e o Rio Paraná inteiro pra vocês.',font=sans(32,'sb'),fill=WH)
x=M
for t in ['25 pés','Até 10 pessoas','Torre de som']: x+=opill(d,x,1130,t)+14
sticker(s,900,300,120,'10','PESSOAS')
cta_bar(d); s.save(OUT+'01-capa.jpg',quality=97)
# 02 SOM
s=grad(pop('9667fb83',W_,H_,cx=0.62,cy=0.45),top=760,bot=560,a1=250,a2=245); d=ImageDraw.Draw(s); brand(s,d,n=2)
d.text((M-4,150),'SOM',font=cond(250),fill=LIME); d.text((M-4,390),'NO TALO.',font=cond(150),fill=WH)
x=M
for t in ['Torre de caixas','Tubos na lateral','Subwoofer']: x+=pill(d,x,1050,t,bg=WH)+14
d.text((M,1140),'A festa vai com vocês pro meio do rio.',font=sans(32,'sb'),fill=WH)
cta_bar(d); s.save(OUT+'02-som.jpg',quality=97)
# 03 BENTO
s=Image.new('RGB',(W_,H_),DK); d=ImageDraw.Draw(s); brand(s,d,n=3)
d.text((M,140),'TUDO A BORDO',font=cond(110),fill=WH)
g=16; X0=M; Y0=290; cw=(W_-2*M-g)//2
def card(im,x,y): tile(s,im,x,y,r=26)
card(pop('3603af94',cw,420,cy=0.25,zoom=1.15),X0,Y0)
d.rounded_rectangle((X0+cw+g,Y0,X0+2*cw+g,Y0+200),radius=26,fill=LIME)
d.text((X0+cw+g+30,Y0+18),'10',font=cond(130),fill=DK); d.text((X0+cw+g+30,Y0+150),'PESSOAS',font=sans(26,'b'),fill=DK)
d.rounded_rectangle((X0+cw+g,Y0+220,X0+2*cw+g,Y0+420),radius=26,fill=DK2)
d.text((X0+cw+g+30,Y0+238),'25',font=cond(130),fill=WH); d.text((X0+cw+g+30,Y0+370),'PÉS · 7,5 M',font=sans(26,'b'),fill=LIME)
card(pop('f6dce81e',cw,520,cy=0.42),X0,Y0+440); card(pop('aafe8b4b',cw,520,cy=0.4),X0+cw+g,Y0+440)
d=ImageDraw.Draw(s)
for (x,y,t) in [(X0+20,Y0+360,'Proa com sofá em U'),(X0+20,Y0+880,'Cockpit'),(X0+cw+g+20,Y0+880,'Popa com som')]: pill(d,x,y,t,bg=WH,f=sans(24,'b'))
cta_bar(d); s.save(OUT+'03-a-bordo.jpg',quality=97)
# 04 PROA
s=grad(pop('3603af94',W_,H_,cy=0.3,zoom=1.25),top=260,bot=860,a1=200,a2=255); d=ImageDraw.Draw(s); brand(s,d,n=4)
d.text((M-4,820),'PROA',font=cond(200),fill=LIME); d.text((M-4,1010),'PRA TURMA.',font=cond(120),fill=WH)
d.text((M,1165),'Sofá em U, porta-copos e caixas de som na proa.',font=sans(30,'sb'),fill=WH)
cta_bar(d); s.save(OUT+'04-proa.jpg',quality=97)
# 05 FICHA
s=Image.new('RGB',(W_,H_),DK); d=ImageDraw.Draw(s); brand(s,d,n=5)
d.text((M,140),'FICHA',font=cond(130),fill=WH); d.text((M+330,140),'NX 250',font=cond(130),fill=LIME)
items=[('25','PÉS','7,5 m de comprimento'),('10','PESSOAS','capacidade no aluguel'),('PROA','ABERTA','com sofá em U'),('SOM','TORRE + SUB','caixas e subwoofer')]
for k,(a_,b_,c_) in enumerate(items):
    x=M+(k%2)*(cw+g); y=330+(k//2)*(340+g)
    d.rounded_rectangle((x,y,x+cw,y+340),radius=26,fill=LIME if k==1 else DK2)
    fg=DK if k==1 else WH; ac=DK if k==1 else LIME
    d.text((x+30,y+20),a_,font=cond(150),fill=fg); d.text((x+32,y+215),b_,font=sans(28,'b'),fill=ac); d.text((x+32,y+262),c_,font=sans(26,'m'),fill=DK if k==1 else GR)
tile(s,pop('1d5d97b3',W_-2*M,230,cy=0.55),M,1040,r=26); d=ImageDraw.Draw(s)
cta_bar(d,H_-80); s.save(OUT+'05-ficha.jpg',quality=97)
# 06 CTA
s=Image.new('RGB',(W_,H_),LIME); d=ImageDraw.Draw(s)
c=lc(110); s.paste(c,(M,40),c); d.text((M+130,66),'COUNTRY',font=wide(32,900),fill=DK); d.text((M+132,106),'N E G Ó C I O S',font=sans(16,'sb'),fill=DK)
d.text((W_-M,80),'6/6',font=sans(26,'b'),fill=DK,anchor='ra')
d.text((M-6,190),'BORA',font=cond(260),fill=DK); d.text((M-6,440),'PRO RIO?',font=cond(200),fill=DK)
tile(s,pop('9667fb83',W_-2*M,330,cy=0.5),M,690,r=30); d=ImageDraw.Draw(s)
d.text((M,1060),'Reserve seu sábado, domingo ou feriado.',font=sans(34,'b'),fill=DK)
d.rounded_rectangle((M,1130,W_-M,1250),radius=60,fill=DK); d.text((540,1190),'(44) 99884-6314',font=cond(76),fill=LIME,anchor='mm')
d.text((540,1290),'ou comente NX',font=sans(28,'b'),fill=DK,anchor='mm')
s.save(OUT+'06-reserve.jpg',quality=97)
# STORY
st=grad(pop('1d5d97b3',1080,1920,cy=0.5),top=520,bot=1200,a1=220,a2=255); d=ImageDraw.Draw(st)
c=lc(150); st.paste(c,(465,70),c)
pill(d,540,260,'ALUGUEL · FIM DE SEMANA',anchor='c')
sticker(st,880,560,115,'10','PESSOAS',rot=10)
d.text((540,1130),'NX 250',font=cond(300),fill=WH,anchor='ma')
d.text((540,1460),'Som alto · 25 pés · proa aberta',font=sans(38,'b'),fill=LIME,anchor='ma')
d.rounded_rectangle((150,1600,930,1720),radius=60,fill=LIME); d.text((540,1660),'RESERVE AGORA',font=cond(72),fill=DK,anchor='mm')
d.text((540,1770),'[ cole o link do WhatsApp aqui ]',font=sans(26,'m'),fill=WH,anchor='ma')
st.save(OUT+'story.jpg',quality=97)
names=['01-capa','02-som','03-a-bordo','04-proa','05-ficha','06-reserve']
ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story.jpg').resize((228,405))]
c=Image.new('RGB',(334*6+238,405),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width+10
c.save('/tmp/claude-0/cn_nx.jpg'); print('ok')
