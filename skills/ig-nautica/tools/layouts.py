import sys; sys.path.insert(0,'.')
from country import *
import kit, rio
OUT='/home/user/instagram-agent-skill/midia/layouts-teste/'
W,H=1080,1350
def load(p):
    J=Image.open(p).convert('RGBA'); return J.crop(J.getbbox())
J230=load('/tmp/claude-0/cut230_25.png'); J170=load('/tmp/claude-0/cut170_25.png')
def rs(J,w): return J.resize((w,int(J.height*w/J.width)),Image.LANCZOS)
def fadebottom(J,frac):
    a=np.array(J).astype(float); h=a.shape[0]; c=int(h*frac); a[...,3]*=np.clip((c-np.arange(h))/(h*0.08),0,1)[:,None]; return Image.fromarray(a.astype('uint8'),'RGBA')
def glass(im,box,col=(14,27,45),alpha=170,blur=18,r=34):
    x0,y0,x1,y1=box; reg=im.crop(box).filter(ImageFilter.GaussianBlur(blur)); im.paste(reg,(x0,y0))
    ov=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle(box,radius=r,fill=col+(alpha,),outline=(255,255,255,40),width=2); im.paste(ov,(0,0),ov)
# ---------- L1 Pôr do sol no rio ----------
bg,hy=rio.scene(W,H,horizon=0.47,sun_x=0.3); J=rs(J230,820)
rio.jet_in_water(bg,J,W-820+20,int(H*0.74)-int(J.height*0.78),wl=0.78)
d=ImageDraw.Draw(bg); L=logo(260); bg.paste(L,(60,56),L)
d.text((66,170),'Sea-Doo',font=sans(40,'sb'),fill=TAG); d.text((60,215),'GTX 230',font=wide(120,900),fill=WHITE)
d.text((66,365),'2025  ·  17 horas  ·  230 hp',font=sans(38,'sb'),fill=WHITE)
glass(bg,(50,1050,1030,1290))
d=ImageDraw.Draw(bg); d.text((90,1080),'R$ 145.000',font=wide(80,900),fill=WHITE)
d.text((92,1190),'Chame no WhatsApp  (44) 99884-6314',font=sans(32,'sb'),fill=TAG)
d.text((W-60,H-34),'imagem ilustrativa',font=sans(20,'m'),fill=(220,220,230),anchor='rs')
bg.save(OUT+'L1-por-do-sol.jpg',quality=95)
# ---------- L2 Oferta varejo ----------
s=kit.studio(W,H,cy=640); d=ImageDraw.Draw(s); L=logo(260); s.paste(L,(60,56),L)
j=fadebottom(rs(J230,900),0.84); kit.place_jet(s,j,W-900+12,330)
rib=Image.new('RGBA',(820,120),(0,0,0,0)); rd=ImageDraw.Draw(rib); rd.rectangle((0,0,820,120),fill=TAG)
rd.text((410,60),'SÓ 17 HORAS',font=wide(64,900),fill=NAVY2,anchor='mm'); rib=rib.rotate(-12,expand=True,resample=Image.BICUBIC)
s.paste(rib,(250,140),rib)
# selo estrela
st=Image.new('RGBA',(300,300),(0,0,0,0)); sd=ImageDraw.Draw(st); pts=[]
for k in range(32):
    r_=140 if k%2==0 else 118; a_=k*math.pi/16; pts.append((150+r_*math.cos(a_),150+r_*math.sin(a_)))
sd.polygon(pts,fill=(232,72,60)); sd.text((150,128),'230',font=wide(70,900),fill=WHITE,anchor='mm'); sd.text((150,190),'CAVALOS',font=sans(26,'b'),fill=WHITE,anchor='mm')
st=st.rotate(10,resample=Image.BICUBIC); s.paste(st,(40,330),st)
d=ImageDraw.Draw(s)
d.rectangle((0,1010,W,H),fill=NAVY2)
d.text((60,1030),'Sea-Doo GTX 230 · 2025',font=sans(40,'sb'),fill=TAG)
d.text((56,1080),'R$ 145 MIL',font=wide(130,900),fill=WHITE)
d.text((60,1250),'Cartão ou cheque, sob consulta · (44) 99884-6314',font=sans(30,'sb'),fill=MUTE)
s.save(OUT+'L2-oferta.jpg',quality=95)
# ---------- L3 Ficha split ----------
s=Image.new('RGB',(W,H),(244,241,235)); d=ImageDraw.Draw(s)
d.rectangle((640,0,W,H),fill=NAVY)
j=fadebottom(rs(J230,760),0.84)
sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).ellipse((0,930,600,1010),fill=120); sh=sh.filter(ImageFilter.GaussianBlur(25)); s.paste((0,0,0),(0,0),sh)
s.paste(j,(-110,520),j); d=ImageDraw.Draw(s)
d.text((60,70),'Sea-Doo',font=sans(40,'sb'),fill=GOLD); d.text((56,115),'GTX',font=wide(130,900),fill=NAVY); d.text((60,260),'230',font=wide(130,900),fill=NAVY)
specs=[('ANO','2025'),('HORAS','17'),('POTÊNCIA','230 hp'),('MOTOR','Supercharger'),('CASCO','ST3 estável'),('FREIO E RÉ','iBR'),('LUGARES','3')]
y=90
for k,v in specs:
    d.text((690,y),k,font=sans(24,'sb'),fill=TAG); d.text((690,y+32),v,font=wide(40,850),fill=WHITE); y+=118
d.line((690,y+5,1030,y+5),fill=GOLD,width=2)
d.text((690,y+25),'R$ 145.000',font=wide(46,900),fill=TAG)
L=logo(230); s.paste(L,(690,H-110),L)
d.text((60,H-80),'(44) 99884-6314',font=wide(36,850),fill=NAVY)
s.save(OUT+'L3-ficha.jpg',quality=95)
# ---------- L4 Revista minimal ----------
s=Image.new('RGB',(W,H),(240,236,228)); d=ImageDraw.Draw(s)
f=wide(330,900); d.text((W/2,170),'GTX',font=f,fill=None,stroke_width=4,stroke_fill=NAVY,anchor='ma') if False else None
mk=Image.new('L',(W,H),0); md=ImageDraw.Draw(mk); md.text((W/2,150),'GTX',font=f,fill=255,anchor='ma',stroke_width=4,stroke_fill=255)
inner=Image.new('L',(W,H),0); ImageDraw.Draw(inner).text((W/2,150),'GTX',font=f,fill=255,anchor='ma')
outline=np.clip(np.array(mk).astype(int)-np.array(inner).astype(int),0,255).astype('uint8')
s.paste(NAVY,(0,0),Image.fromarray(outline))
j=fadebottom(rs(J230,1000),0.84)
sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).ellipse((140,1040,1060,1110),fill=110); sh=sh.filter(ImageFilter.GaussianBlur(25)); s.paste((0,0,0),(0,0),sh)
s.paste(j,(W-1000+12,430),j); d=ImageDraw.Draw(s)
d.text((60,60),'COUNTRY NEGÓCIOS',font=sans(26,'sb'),fill=GOLD); d.text((W-60,60),'EDIÇÃO VERÃO',font=sans(26,'sb'),fill=GOLD,anchor='ra')
d.line((60,1150,W-60,1150),fill=NAVY,width=2)
cols=[('Modelo','Sea-Doo GTX 230'),('Ano / Horas','2025 · 17 h'),('Valor','R$ 145.000')]
for i,(k,v) in enumerate(cols):
    x=60+i*330; d.text((x,1170),k,font=sans(24,'m'),fill=(120,120,130)); d.text((x,1205),v,font=sans(34,'b'),fill=NAVY)
d.text((60,1285),'WhatsApp (44) 99884-6314',font=sans(28,'sb'),fill=GOLD)
s.save(OUT+'L4-revista.jpg',quality=95)
# ---------- L5 Loja x Rio ----------
s=Image.new('RGB',(W,H),NAVY); top,hy2=rio.scene(W,700,horizon=0.45,sun_x=0.28)
jt=rs(J230,600); rio.jet_in_water(top,jt,W-600+20,int(700*0.86)-int(jt.height*0.78),wl=0.78); s.paste(top,(0,0))
src=Image.open('/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/a35958ff-image.jpg').convert('RGB')
bgp=src.resize((1080,1440)).crop((0,330,1080,1000)).filter(ImageFilter.GaussianBlur(40)); bgp=ImageEnhance.Brightness(bgp).enhance(0.8)
jb=rs(J230,700); bgp.paste(jb,(W-700+12,90),jb); s.paste(bgp,(0,700))
d=ImageDraw.Draw(s); d.rectangle((0,690,W,712),fill=TAG)
for (y,t1) in [(40,'NO SEU FIM DE SEMANA'),(740,'HOJE NA COUNTRY')]:
    tw_=d.textlength(t1,font=sans(30,'b')); d.rounded_rectangle((50,y,50+tw_+40,y+56),radius=28,fill=NAVY2); d.text((70,y+12),t1,font=sans(30,'b'),fill=TAG)
glass(s,(50,1150,1030,1310),alpha=200)
d=ImageDraw.Draw(s); d.text((90,1170),'GTX 230 · 2025 · 17 h',font=wide(44,850),fill=WHITE); d.text((90,1235),'R$ 145.000  ·  (44) 99884-6314',font=sans(34,'sb'),fill=TAG)
d.text((W-60,670),'imagem ilustrativa',font=sans(20,'m'),fill=(230,230,235),anchor='rs')
s.save(OUT+'L5-loja-x-rio.jpg',quality=95)
# ---------- L6 Qual você escolhe ----------
s=kit.studio(W,H,cy=700); d=ImageDraw.Draw(s); L=logo(260); s.paste(L,(410,50),L)
d.text((W/2,170),'Qual você leva?',font=wide(72,900),fill=WHITE,anchor='ma')
d.line((W/2,300,W/2,1250),fill=GOLD,width=3)
for i,(J,mod,ano,hrs,hp,pr) in enumerate([(J170,'GTX 170','2025','29 h','170 hp','R$ 135 mil'),(J230,'GTX 230','2025','17 h','230 hp','R$ 145 mil')]):
    cx=270+i*540; j=fadebottom(rs(J,480),0.9); kit.place_jet(s,j,cx-240,360,refl=False)
    d=ImageDraw.Draw(s); d.text((cx,760),mod,font=wide(56,900),fill=WHITE,anchor='ma')
    for k,(a_,b_) in enumerate([('Ano',ano),('Horas',hrs),('Potência',hp)]):
        d.text((cx-170,860+k*70),a_,font=sans(30,'m'),fill=MUTE); d.text((cx+170,860+k*70),b_,font=sans(32,'b'),fill=WHITE,anchor='ra')
    d.rounded_rectangle((cx-200,1090,cx+200,1180),radius=45,fill=TAG); d.text((cx,1135),pr,font=wide(40,900),fill=NAVY2,anchor='mm')
d.text((W/2,1240),'Comente 170 ou 230 que a gente te chama',font=sans(32,'sb'),fill=WHITE,anchor='ma')
s.save(OUT+'L6-qual-voce-leva.jpg',quality=95)
names=['L1-por-do-sol','L2-oferta','L3-ficha','L4-revista','L5-loja-x-rio','L6-qual-voce-leva']
ims=[Image.open(OUT+n+'.jpg').resize((432,540)) for n in names]
c=Image.new('RGB',(442*3,550*2),'white')
for i,im in enumerate(ims): c.paste(im,((i%3)*442,(i//3)*550))
c.save('/tmp/claude-0/layouts_prev.jpg'); print('ok')
