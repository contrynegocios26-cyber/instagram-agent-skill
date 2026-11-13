import sys; sys.path.insert(0,'.')
from kit import *
W,H=1080,1350
def num(d,i,dark=True): d.text((W-96,H-64),f'{i}/5',font=f('m',28),fill=MUTE if dark else (140,145,160))
def brand(s,d,dark=True):
    s.paste(icon(58),(56,H-58-44),icon(58)); d.text((128,H-44-46),'COUNTRY NEGÓCIOS',font=f('b',26),fill=WHITE if dark else NAVY)

# 1 CAPA: texto atrás do jet
s=studio(W,H,cy=760); d=ImageDraw.Draw(s)
ctext(d,64,'SEA-DOO GTI 2024 · SEMINOVO',f('b',36),GOLD2,sp=8)
g,mk=gold_text(W,H,0,0,'89h',f('black',470)); 
bb=mk.getbbox(); m2=Image.new('L',(W,H),0); m2.paste(mk.crop(bb),(int((W-(bb[2]-bb[0]))/2),140)); 
g,_=gold_text(W,H,0,0,'89',f('black',560)); g2=Image.new('RGB',(W,H)); 
# regenerate gradient aligned to placed mask
gy=np.clip((np.arange(H)-140)/(bb[3]-bb[1]),0,1)[:,None,None]; arr=(np.array(GOLD2)*(1-gy)+np.array((150,110,60))*gy); arr=np.repeat(arr,W,1).astype('uint8')
s.paste(Image.fromarray(arr,'RGB'),(0,0),m2)
d.text((W/2+ (bb[2]-bb[0])/2 - 10, 190),'HORAS',font=f('black',58),fill=WHITE,anchor='ra') if False else None
j=jet(820); place_jet(s,j,(W-820)/2,430)
d=ImageDraw.Draw(s)
# bottom bar
ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
for i in range(260): od.line((0,H-260+i,W,H-260+i),fill=DEEP+(int(235*i/260),))
s.paste(ov,(0,0),ov); d=ImageDraw.Draw(s)
ctext(d,H-250,'R$ 105 mil',f('black',100),WHITE)
pill(d,W/2,H-128,'em até 18x no cartão',f('xb',40),GOLD,DEEP)
s.paste(icon(64),(44,H-64-40),icon(64)); num(d,1)
s.save(OUT+'p1-capa.jpg',quality=95)

# 2 POR QUE ESSE
s=studio(W,H,cy=360,glow=0.7); d=ImageDraw.Draw(s)
ctext(d,80,'POR QUE ESSE JET',f('b',36),GOLD2,sp=8)
ctext(d,130,'vale cada centavo',f('black',84),WHITE)
j=jet(620); place_jet(s,j,(W-620)/2,250,refl=False)
d=ImageDraw.Draw(s)
cards=[('89 h','Pouco uso, motor quase novo.'),('2024','Modelo atual da Sea-Doo.'),('3 lugares','Leva a família ou os amigos.')]
y=830
for big,txt in cards:
    d.rounded_rectangle((70,y,W-70,y+128),radius=26,fill=(16,30,50),outline=(70,95,125),width=2)
    d.text((105,y+34),big,font=f('black',54),fill=GOLD2)
    d.text((390,y+46),txt,font=f('m',34),fill=WHITE)
    y+=148
brand(s,d); num(d,2); s.save(OUT+'p2-porque.jpg',quality=95)

# 3 CALLOUTS
s=studio(W,H,cy=700); d=ImageDraw.Draw(s)
ctext(d,80,'CONHEÇA O GTI',f('b',36),GOLD2,sp=8)
ctext(d,130,'Sea-Doo GTI 2024',f('black',84),WHITE)
jw=760; j=jet(jw); jx=50; jy=430; place_jet(s,j,jx,jy); d=ImageDraw.Draw(s)
sc_=jw/800
def call(px,py,ty,t1,t2):
    X,Y=jx+px*sc_,jy+py*sc_; tx=830
    d.ellipse((X-10,Y-10,X+10,Y+10),fill=GOLD2); d.ellipse((X-21,Y-21,X+21,Y+21),outline=GOLD2,width=3)
    d.line((X,Y,tx,ty),fill=GOLD2,width=3); d.line((tx,ty,1030,ty),fill=GOLD2,width=3)
    d.text((840,ty-62),t1,font=f('black',54),fill=WHITE); d.text((840,ty+10),t2,font=f('m',30),fill=MUTE)
call(610,165,420,'89 h','de motor')
call(640,250,660,'3','lugares')
call(270,305,900,'2024','modelo atual')
brand(s,d); num(d,3); s.save(OUT+'p3-detalhes.jpg',quality=95)

# 4 CONDICOES
s=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(s)
ctext(d,110,'CONDIÇÕES',f('b',38),GOLD,sp=10)
ctext(d,190,'R$ 105.000',f('black',128),NAVY); ctext(d,350,'à vista',f('m',42),(100,110,125))
d.line((260,450,820,450),fill=GOLD,width=3)
ctext(d,500,'ou em até',f('m',46),(100,110,125))
g_,_=None,None
mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).text((W/2,560),'18x',font=f('black',300),fill=255,anchor='ma')
bb=mk.getbbox(); gy=np.clip((np.arange(H)-bb[1])/(bb[3]-bb[1]),0,1)[:,None,None]
arr=np.repeat(np.array((40,70,108))*(1-gy)+np.array(NAVY)*gy,W,1).astype('uint8'); s.paste(Image.fromarray(arr,'RGB'),(0,0),mk)
ctext(d,900,'no cartão de crédito',f('xb',54),NAVY)
pill(d,W/2,1030,'Chama no WhatsApp',f('xb',44),NAVY,WHITE,h=96)
brand(s,d,False); d.text((W-96,H-64),'4/5',font=f('m',28),fill=(140,145,160))
s.save(OUT+'p4-condicoes.jpg',quality=95)

# 5 CTA
s=studio(W,H,cy=560); d=ImageDraw.Draw(s)
ctext(d,90,'Seu verão',f('black',112),WHITE); ctext(d,215,'começa aqui.',f('black',112),GOLD2)
j=jet(720); place_jet(s,j,(W-720)/2,390); d=ImageDraw.Draw(s)
ctext(d,1035,'Comente EU QUERO',f('black',64),WHITE)
ctext(d,1118,'e a gente te chama no direct',f('m',38),MUTE)
brand(s,d); num(d,5); s.save(OUT+'p5-cta.jpg',quality=95)

ims=[Image.open(OUT+x).resize((432,540)) for x in ['p1-capa.jpg','p2-porque.jpg','p3-detalhes.jpg','p4-condicoes.jpg','p5-cta.jpg']]
c=Image.new('RGB',(432*5+40,540),'white'); 
for i,im in enumerate(ims): c.paste(im,(i*442,0))
c.save('prev_car.jpg'); print('ok')
