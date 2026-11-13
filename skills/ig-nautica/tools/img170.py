import sys; sys.path.insert(0,'.')
from country import *
import kit
OUT='/home/user/instagram-agent-skill/midia/2026-11-13-gti170-2025/'
J=Image.open('/tmp/claude-0/j170_final.png'); OFF=(72,214)
def portrait():
    p=Image.open('/tmp/claude-0/photo170_clean.jpg').convert('RGB')
    bg=p.filter(ImageFilter.GaussianBlur(16)); bg=ImageEnhance.Brightness(bg).enhance(0.9); bg.paste(J,OFF,J)
    bg=ImageEnhance.Contrast(bg).enhance(1.1); bg=ImageEnhance.Color(bg).enhance(1.15); return bg.filter(ImageFilter.UnsharpMask(2,60,2))
P=portrait(); P.save('/tmp/claude-0/p170_portrait.jpg',quality=95)
# kit studio jet
a=np.array(J).astype(float); Hh=a.shape[0]; fade=np.clip((735-np.arange(Hh))/100,0,1)[:,None]; a[...,3]*=fade
SJ=Image.fromarray(a.astype('uint8'),'RGBA').crop((0,0,800,735)); SJ=ImageEnhance.Contrast(SJ).enhance(1.08); SJ=ImageEnhance.Color(SJ).enhance(1.15)
SJ.save('/tmp/claude-0/j170_studio.png')
def sj(w): return SJ.resize((w,int(SJ.height*w/SJ.width)),Image.LANCZOS)
W,H=1080,1350
COLS=[('Ano','2025'),('Horas de uso','41'),('Potência','170 hp')]
def base(ct,panel,h=H):
    ph=P.resize((1080,1920),Image.LANCZOS).crop((0,ct,1080,ct+h)); fade_to_navy(ph,panel-200,panel); return ph
def num(d,i,n=7,w=W,h=H): d.text((w-96,h-60),f'{i}/{n}',font=sans(26,'m'),fill=MUTE)
# 1 capa
s=base(300,880); d=ImageDraw.Draw(s)
d.text((72,905),'Sea-Doo',font=sans(40,'sb'),fill=GOLD); d.text((68,962),'GTI 170',font=wide(104,850),fill=WHITE)
d.line((72,1100,1008,1100),fill=GOLD,width=3); info_cols(d,1120,COLS); footer(s,d,1238)
t=tag('110.000','modelo 2025',w=390,angle=6); s.paste(t,(495,650),t); s.save(OUT+'01-capa.jpg',quality=95)
# 2 horas
s=base(130,1000); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
d.text((66,1015),'41 horas',font=wide(150,850),fill=WHITE)
d.text((72,1185),'É tudo que ele navegou.',font=sans(42,'sb'),fill=WHITE)
d.text((72,1240),'Sea-Doo GTI 170 · 2025 · Midnight Purple',font=sans(32,'m'),fill=MUTE)
d.text((72,1290),'Arraste para conhecer →',font=sans(28,'sb'),fill=GOLD); s.save(OUT+'02-horas.jpg',quality=95)
# 3 motor
s=kit.studio(W,H,cy=760); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).text((W/2,190),'170',font=wide(330,900),fill=255,anchor='ma')
bb=mk.getbbox(); gy=np.clip((np.arange(H)-bb[1])/(bb[3]-bb[1]),0,1)[:,None,None]
arr=np.repeat(np.array((236,205,150))*(1-gy)+np.array((160,118,62))*gy,W,1).astype('uint8'); s.paste(Image.fromarray(arr,'RGB'),(0,0),mk)
d.text((W/2,520),'CAVALOS',font=wide(56,850),fill=WHITE,anchor='ma')
kit.place_jet(s,sj(760),160,600); d=ImageDraw.Draw(s)
ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
for i in range(280): od.line((0,H-280+i,W,H-280+i),fill=NAVY+(int(240*i/280),))
s.paste(ov,(0,0),ov); d=ImageDraw.Draw(s)
d.text((72,1150),'Motor Rotax® 1630 ACE™',font=wide(44,800),fill=WHITE)
d.text((72,1210),'O mais potente aspirado da Sea-Doo.',font=sans(34,'m'),fill=MUTE); num(d,3); s.save(OUT+'03-motor.jpg',quality=95)
# 4 o que ele tem
s=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
d.text((72,200),'O que ele tem',font=sans(40,'sb'),fill=GOLD); d.text((68,250),'Equipado de fábrica',font=wide(64,850),fill=WHITE)
feats=[('iBR','Freio e ré eletrônicos'),('iTC','Acelerador inteligente'),('VTS','Trim ajustável no guidão'),('ECO / Sport','Modos de pilotagem'),('Regulador','Velocidade constante'),('Painel','Digital de 4,5"'),('3 lugares','Escada de embarque'),('LinQ','Encaixe de acessórios')]
y=400
for k,v in feats:
    d.rounded_rectangle((72,y,1008,y+84),radius=18,fill=(30,50,77))
    d.text((100,y+20),k,font=wide(34,850),fill=TAG); d.text((420,y+24),v,font=sans(32,'m'),fill=WHITE); y+=96
d.text((72,1190),'Itens de série do GTI SE 170 2025, conforme ficha da BRP.',font=sans(24,'m'),fill=(130,145,165))
num(d,4); s.save(OUT+'04-equipamentos.jpg',quality=95)
# 5 callouts studio
s=kit.studio(W,H,cy=700); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
d.text((72,190),'Conheça o GTI 170',font=wide(60,850),fill=WHITE)
jw=760; jx,jy=40,420; kit.place_jet(s,sj(jw),jx,jy); d=ImageDraw.Draw(s); sc=jw/800
def call(px,py,ty,t1,t2):
    X,Y=jx+px*sc,jy+py*sc; tx=820
    d.ellipse((X-10,Y-10,X+10,Y+10),fill=TAG); d.ellipse((X-21,Y-21,X+21,Y+21),outline=TAG,width=3)
    d.line((X,Y,tx,ty),fill=TAG,width=3); d.line((tx,ty,1030,ty),fill=TAG,width=3)
    d.text((830,ty-58),t1,font=wide(44,850),fill=WHITE); d.text((830,ty+10),t2,font=sans(28,'m'),fill=MUTE)
call(575,128,390,'Painel','digital 4,5"')
call(600,215,640,'3','lugares')
call(330,600,900,'170 hp','Rotax 1630')
d.text((72,1190),'41 horas · modelo 2025',font=sans(34,'sb'),fill=TAG); num(d,5); s.save(OUT+'05-detalhes.jpg',quality=95)
# 6 condicoes
s=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
d.text((72,250),'Condições',font=sans(40,'sb'),fill=GOLD); d.text((68,305),'R$ 110.000',font=wide(112,850),fill=WHITE)
d.line((72,480,1008,480),fill=GOLD,width=3)
d.text((72,530),'Pagamento no cartão ou',font=wide(50,800),fill=WHITE); d.text((72,600),'cheque, sob consulta.',font=wide(50,800),fill=WHITE)
d.text((72,720),'Chame no WhatsApp e receba o vídeo',font=sans(36,'m'),fill=MUTE); d.text((72,768),'dele funcionando.',font=sans(36,'m'),fill=MUTE)
d.line((72,1100,1008,1100),fill=GOLD,width=3); info_cols(d,1120,COLS); footer(s,d,1238); s.save(OUT+'06-condicoes.jpg',quality=95)
# 7 CTA
s=base(280,820); d=ImageDraw.Draw(s)
d.text((68,880),'Seu verão',font=wide(96,850),fill=WHITE); d.text((68,985),'começa aqui.',font=wide(96,850),fill=TAG)
d.line((72,1120,1008,1120),fill=GOLD,width=3); d.text((72,1145),'Comente EU QUERO ou chame no WhatsApp',font=sans(30,'sb'),fill=WHITE)
L=logo(250); s.paste(L,(72,1215),L); t2='(44) 99884-6314'; d.text((1008-d.textlength(t2,font=wide(34,800)),1245),t2,font=wide(34,800),fill=WHITE)
s.save(OUT+'07-cta.jpg',quality=95)
# QUADRADO 1080x1080 (Facebook / Marketplace)
q=P.resize((1080,1920),Image.LANCZOS).crop((0,330,1080,1410)); fade_to_navy(q,560,740); d=ImageDraw.Draw(q)
d.text((72,690),'Sea-Doo',font=sans(36,'sb'),fill=GOLD); d.text((68,738),'GTI 170',font=wide(88,850),fill=WHITE)
d.line((72,862,1008,862),fill=GOLD,width=3); info_cols(d,878,COLS); footer(q,d,982)
t=tag('110.000','modelo 2025',w=360,angle=6); q.paste(t,(540,450),t); q.save(OUT+'quadrado-facebook.jpg',quality=95)
# STORY 1 oferta
st=P.resize((1080,1920),Image.LANCZOS); fade_to_navy(st,1150,1400); d=ImageDraw.Draw(st)
top=Image.new('RGBA',(1080,420),(0,0,0,0)); td=ImageDraw.Draw(top)
for y in range(420): td.line((0,y,1080,y),fill=NAVY+(int(200*(1-y/420)),))
st.paste(top,(0,0),top); L=logo(300); st.paste(L,(390,110),L)
d.text((72,1420),'Sea-Doo',font=sans(44,'sb'),fill=GOLD); d.text((68,1485),'GTI 170',font=wide(104,850),fill=WHITE)
d.line((72,1640,1008,1640),fill=GOLD,width=3); info_cols(d,1665,COLS)
t=tag('110.000','modelo 2025',w=400,angle=6); st.paste(t,(480,1150),t)
d.rounded_rectangle((72,1800,1008,1880),radius=40,outline=WHITE,width=3)
tx='[ cole aqui o link do WhatsApp ]'; d.text((540-d.textlength(tx,font=sans(30,'m'))/2,1822),tx,font=sans(30,'m'),fill=MUTE)
st.save(OUT+'story-1-oferta.jpg',quality=95)
# STORY 2 quiz
st=kit.studio(1080,1920,cy=1000); d=ImageDraw.Draw(st); L=logo(300); st.paste(L,(390,110),L)
d.text((540,330),'QUIZ',font=sans(44,'sb'),fill=GOLD,anchor='ma'); d.text((540,400),'Quantas horas',font=wide(84,850),fill=WHITE,anchor='ma'); d.text((540,500),'tem esse jet?',font=wide(84,850),fill=WHITE,anchor='ma')
kit.place_jet(st,sj(900),90,700); d=ImageDraw.Draw(st)
d.rounded_rectangle((140,1560,940,1700),radius=30,outline=TAG,width=3)
tx='[ coloque aqui a figurinha QUIZ: 41 / 150 / 300 ]'; d.text((540,1630),tx,font=sans(28,'m'),fill=MUTE,anchor='mm')
st.save(OUT+'story-2-quiz.jpg',quality=95)
names=['01-capa','02-horas','03-motor','04-equipamentos','05-detalhes','06-condicoes','07-cta']
ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]
c=Image.new('RGB',(334*7,405+10+400),'white')
for i,im in enumerate(ims): c.paste(im,(i*334,0))
extra=[Image.open(OUT+'quadrado-facebook.jpg').resize((400,400)),Image.open(OUT+'story-1-oferta.jpg').resize((225,400)),Image.open(OUT+'story-2-quiz.jpg').resize((225,400))]
x=0
for im in extra: c.paste(im,(x,415)); x+=im.width+10
c.save('prev170.jpg'); print('ok')
