import sys,os; sys.path.insert(0,'.')
from country import *
os.makedirs(OUT,exist_ok=True)
W,H=1080,1350
P=photo_portrait()  # 900x1600
def base(crop_top=200, panel=860):
    ph=P.resize((1080,1920),Image.LANCZOS).crop((0,crop_top,1080,crop_top+H))
    fade_to_navy(ph,panel-200,panel); return ph

# ---- 1 CAPA (padrão do perfil) ----
s=base(330,880); d=ImageDraw.Draw(s)
d.text((72,905),'Sea-Doo',font=sans(40,'sb'),fill=GOLD)
d.text((68,962),'GTI 2024',font=wide(86,850),fill=WHITE)
d.line((72,1100,1008,1100),fill=GOLD,width=3)
info_cols(d,1120,[('Ano','2024'),('Horas de uso','89'),('Lugares','3')])
footer(s,d,1238)
t=tag('105.000','ou 18x no cartão',w=390,angle=6); s.paste(t,(495,650),t)
s.save(OUT+'01-capa.jpg',quality=95)

# ---- 2 HORAS (estilo do post "63 horas") ----
s=base(120,1000); d=ImageDraw.Draw(s)
L=logo(300); s.paste(L,(60,56),L)
d.text((66,1015),'89 horas',font=wide(150,850),fill=WHITE)
d.text((72,1185),'É tudo que ele navegou.',font=sans(42,'sb'),fill=WHITE)
d.text((72,1240),'Sea-Doo GTI 2024 · 3 lugares',font=sans(32,'m'),fill=MUTE)
d.text((72,1290),'Arraste para conhecer →',font=sans(28,'sb'),fill=GOLD)
s.save(OUT+'02-horas.jpg',quality=95)

# ---- 3 DETALHE (foto aproximada) ----
ph=P.resize((1620,2880),Image.LANCZOS).crop((270,480,1350,1830)); fade_to_navy(ph,980,1180)
d=ImageDraw.Draw(ph); L=logo(300); ph.paste(L,(60,56),L)
d.text((72,1195),'Modelo atual, pronto pro verão.',font=sans(40,'sb'),fill=WHITE)
d.text((72,1250),'Seminovo · Sea-Doo GTI 2024',font=sans(30,'m'),fill=MUTE)
ph.save(OUT+'03-detalhe.jpg',quality=95)

# ---- 4 CONDIÇÕES (painel navy) ----
s=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(s)
L=logo(300); s.paste(L,(60,56),L)
d.text((72,250),'Condições',font=sans(40,'sb'),fill=GOLD)
d.text((68,305),'R$ 105.000',font=wide(112,850),fill=WHITE)
d.text((72,450),'à vista',font=sans(36,'m'),fill=MUTE)
d.line((72,540,1008,540),fill=GOLD,width=3)
d.text((72,580),'ou parcelado em até',font=sans(40,'m'),fill=WHITE)
d.text((60,630),'18x',font=wide(300,900),fill=TAG)
d.text((72,950),'no cartão de crédito',font=wide(54,800),fill=WHITE)
d.line((72,1100,1008,1100),fill=GOLD,width=3)
info_cols(d,1120,[('Modelo','GTI'),('Ano','2024'),('Horas de uso','89')])
footer(s,d,1238); s.save(OUT+'04-condicoes.jpg',quality=95)

# ---- 5 CTA ----
s=base(300,820); d=ImageDraw.Draw(s)
d.text((68,880),'Seu verão',font=wide(96,850),fill=WHITE)
d.text((68,985),'começa aqui.',font=wide(96,850),fill=TAG)
d.line((72,1120,1008,1120),fill=GOLD,width=3)
d.text((72,1145),'Comente EU QUERO ou chame no WhatsApp',font=sans(30,'sb'),fill=WHITE)
footer(s,d,1238) if False else None
L=logo(250); s.paste(L,(72,1215),L)
t2='(44) 99884-6314'; d.text((1008-d.textlength(t2,font=wide(34,800)),1245),t2,font=wide(34,800),fill=WHITE)
s.save(OUT+'05-cta.jpg',quality=95)

# ---- STORY 1080x1920 ----
st=P.resize((1080,1920),Image.LANCZOS); 
ov=Image.new('L',(1080,1920),0); 
fade_to_navy(st,1150,1400); d=ImageDraw.Draw(st)
top=Image.new('RGBA',(1080,420),(0,0,0,0)); td=ImageDraw.Draw(top)
for y in range(420): td.line((0,y,1080,y),fill=NAVY+(int(200*(1-y/420)),))
st.paste(top,(0,0),top); L=logo(300); st.paste(L,(390,110),L)
d.text((72,1420),'Sea-Doo',font=sans(44,'sb'),fill=GOLD)
d.text((68,1485),'GTI 2024',font=wide(92,850),fill=WHITE)
d.line((72,1640,1008,1640),fill=GOLD,width=3)
info_cols(d,1665,[('Ano','2024'),('Horas de uso','89'),('Lugares','3')])
t=tag('105.000','ou 18x no cartão',w=400,angle=6); st.paste(t,(480,1150),t)
d.rounded_rectangle((72,1800,1008,1880),radius=40,outline=WHITE,width=3)
tx='[ cole aqui o link do WhatsApp ]'; d.text((540-d.textlength(tx,font=sans(30,'m'))/2,1822),tx,font=sans(30,'m'),fill=MUTE)
st.save(OUT+'story.jpg',quality=95)

names=['01-capa','02-horas','03-detalhe','04-condicoes','05-cta']
ims=[Image.open(OUT+n+'.jpg').resize((432,540)) for n in names]+[Image.open(OUT+'story.jpg').resize((304,540))]
c=Image.new('RGB',(432*5+304+60,540),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width+10
c.save('prev_country.jpg'); print('ok')
