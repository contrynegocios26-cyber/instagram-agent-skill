import sys; sys.path.insert(0,'.')
from motor import *
import real, kit
B='/tmp/claude-0/aen/b/'; SRD='/tmp/claude-0/aen/sr/'
OUT='/home/user/instagram-agent-skill/midia/miami-do-parana/'
def crop(path,W_,H_,cx=0.5,cy=0.5,zoom=1.0):
    im=Image.open(path).convert('RGB'); iw,ih=im.size; r=W_/H_; ch=int(ih/zoom); cw=int(ch*r)
    if cw>iw: cw=iw; ch=int(cw/r)
    x0=int(min(max(iw*cx-cw/2,0),iw-cw)); y0=int(min(max(ih*cy-ch/2,0),ih-ch))
    return im.crop((x0,y0,x0+cw,y0+ch)).resize((W_,H_),Image.LANCZOS)
def cut(p,bottom=None):
    J=Image.open(p).convert('RGBA'); J=J.crop(J.getbbox())
    if bottom:
        a=np.array(J).astype(float); h=a.shape[0]; c=int(h*bottom); a[...,3]*=np.clip((c-np.arange(h))/6,0,1)[:,None]; J=Image.fromarray(a.astype('uint8'),'RGBA')
    return J
def rs(J,w): return J.resize((w,int(J.height*w/J.width)),Image.LANCZOS)
CREDIT='Fotos de Porto Rico: Roberto Dziura Jr./AEN (domínio público)'
def credit(im): ImageDraw.Draw(im).text((im.width/2,im.height-22),CREDIT,font=sans(17,'m'),fill=(235,238,240),anchor='mm',stroke_width=2,stroke_fill=(20,25,30))
def shade(im,top=420,bot=0,a1=190,a2=0):
    im=im.convert('RGBA'); W_,H_=im.size; ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top): d.line((0,y,W_,y),fill=NAVY2+(int(a1*(1-y/top)),))
    for y in range(bot): d.line((0,H_-y,W_,H_-y),fill=NAVY2+(int(a2*(1-y/bot)),))
    im.alpha_composite(ov); return im.convert('RGB')
def T(d,xy,txt,f,fill,anchor='la',sw=4): d.text(xy,txt,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=NAVY2)
SUNSET={'tint':(1.10,0.88,0.74),'bright':0.72,'contrast':1.18,'sat':0.95}
JETS=[('jet_final.png','GTI','2024','89 h','R$ 105 mil',None),('j170_final.png','GTI 170','2025','41 h','R$ 110 mil',None),
 ('cut230.png','GTX 230','2020','105 h','R$ 120 mil',0.92),('cut170g.png','GTX 170','2024','39 h','R$ 135 mil',0.78),
 ('cut170_25.png','GTX 170','2025','29 h','R$ 135 mil',0.88),('cut170_47c.png','GTX 170','2025','47 h','R$ 135 mil',0.92),
 ('cut230_25.png','GTX 230','2025','17 h','R$ 145 mil',0.82)]
JC=[(cut('/tmp/claude-0/'+f,b),m,a,h,p) for f,m,a,h,p,b in JETS]
J230=cut('/tmp/claude-0/cut230_25.png',0.82); J170=cut('/tmp/claude-0/cut170_25.png',0.9)
W_,H_=1080,1350
if 'img' in sys.argv:
    # 1 capa cidade
    s=shade(crop(B+'protorico_cidade_foto_rdziura-2404.jpg',W_,H_,cx=0.62,cy=0.45),top=620,bot=380,a1=210,a2=200); d=ImageDraw.Draw(s)
    L=logo(250); s.paste(L,(60,50),L)
    T(d,(60,190),'Porto Rico · PR',sans(40,'sb'),TAG); T(d,(54,240),'MIAMI',wide(170,900),WHITE); T(d,(58,420),'DO PARANÁ',wide(92,900),TAG)
    T(d,(60,1110),'Seu lugar aqui começa',wide(48,850),WHITE); T(d,(60,1170),'na Country.',wide(48,850),TAG); T(d,(60,1250),'Arraste →',sans(32,'sb'),WHITE)
    credit(s); s.save(OUT+'01-miami-do-parana.jpg',quality=96)
    # 2 prainha +4 mil
    s=shade(crop(B+'protorico_aereas_foto_rdziura-0109.jpg',W_,H_,cx=0.45),top=560,a1=210); d=ImageDraw.Draw(s)
    T(d,(60,80),'+ de 4 mil',wide(130,900),WHITE); T(d,(60,240),'embarcações',wide(80,900),TAG)
    T(d,(62,360),'Porto Rico é a cidade do Paraná com mais',sans(36,'sb'),WHITE); T(d,(62,408),'barcos registrados na Marinha.*',sans(36,'sb'),WHITE)
    T(d,(62,H_-70),'*Segundo o Governo do Paraná.',sans(24,'m'),WHITE,sw=3); credit(s); s.save(OUT+'02-4-mil-embarcacoes.jpg',quality=96)
    # 3 pôr do sol real (sem montagem)
    s=shade(crop(B+'portorico_pordosol_foto_rdziura-0060.jpg',W_,H_,cx=0.5,cy=0.5),top=430,bot=300,a1=170,a2=170); d=ImageDraw.Draw(s)
    T(d,(60,90),'O pôr do sol',wide(92,900),WHITE); T(d,(60,205),'que vale a viagem.',wide(66,900),TAG)
    T(d,(62,310),'Rio Paraná · Porto Rico',sans(36,'sb'),WHITE); credit(s); s.save(OUT+'03-por-do-sol.jpg',quality=96)
    # 4 só falta o seu jet: cenário real em cima, jet em estúdio embaixo
    s=Image.new('RGB',(W_,H_),NAVY)
    top=shade(real.bg_crop('ilha_carioca_foto_rdzura-1754.jpg',W_,640,cx_frac=0.5,cy_frac=0.42),top=300,a1=170); s.paste(top,(0,0))
    d=ImageDraw.Draw(s); T(d,(60,70),'Só falta',wide(100,900),WHITE); T(d,(60,190),'o seu jet.',wide(100,900),TAG)
    pw=d.textlength('Prainha de Santa Rosa',font=sans(30,'sb')); d.rounded_rectangle((60,540,60+pw+80,598),radius=29,fill=WHITE)
    d.ellipse((80,557,104,581),fill=(220,60,50)); d.ellipse((88,565,96,573),fill=WHITE); d.text((116,552),'Prainha de Santa Rosa',font=sans(30,'sb'),fill=NAVY2)
    d.rectangle((0,640,W_,646),fill=TAG)
    st=kit.studio(W_,H_-646,cy=360); kit.place_jet(st,rs(J230,600),W_-600+12,60); s.paste(st,(0,646))
    d=ImageDraw.Draw(s); d.text((60,700),'Sea-Doo',font=sans(36,'sb'),fill=TAG); d.text((56,745),'GTX 230',font=wide(84,900),fill=WHITE)
    d.text((60,880),'2025 · 17 horas',font=sans(36,'sb'),fill=WHITE); d.text((60,930),'230 hp',font=sans(36,'sb'),fill=WHITE)
    d.rounded_rectangle((60,1010,420,1100),radius=45,fill=TAG); d.text((240,1055),'R$ 145 mil',font=wide(44,900),fill=NAVY2,anchor='mm')
    L=logo(240); s.paste(L,(60,1200),L); d.text((1020,1230),'(44) 99884-6314',font=wide(36,850),fill=WHITE,anchor='ra')
    credit(s); s.save(OUT+'04-so-falta-o-seu.jpg',quality=96)
    # 5 escolha o seu
    s=kit.studio(W_,H_,cy=600); d=ImageDraw.Draw(s); L=logo(250); s.paste(L,(60,50),L)
    d.text((60,150),'Escolha o seu',font=wide(76,900),fill=WHITE); d.text((62,255),'Pronta entrega na Country',font=sans(34,'sb'),fill=TAG)
    y=330
    for (J,m,a,h,p) in JC:
        d.rounded_rectangle((50,y,1030,y+128),radius=22,fill=(16,30,50),outline=(60,85,115),width=2)
        th=rs(J,170); th=th.crop((0,0,170,min(th.height,118))); s.paste(th,(70,y+5),th)
        d.text((270,y+22),f'Sea-Doo {m}',font=wide(40,850),fill=WHITE); d.text((272,y+76),f'{a} · {h}',font=sans(30,'m'),fill=MUTE)
        d.text((1005,y+44),p,font=wide(40,900),fill=TAG,anchor='ra'); y+=138
    s.save(OUT+'05-escolha-o-seu.jpg',quality=96)
    # 6 CTA
    s=shade(crop(B+'portorico_pordosol_foto_rdziura-0076.jpg',W_,H_,cx=0.5,cy=0.5),top=0,bot=900,a2=235); d=ImageDraw.Draw(s)
    L=logo(560); s.paste(L,(260,560),L)
    T(d,(540,770),'Seu lugar na Miami do Paraná',wide(50,900),WHITE,'ma'); T(d,(540,840),'começa aqui.',wide(50,900),TAG,'ma')
    d.line((140,940,940,940),fill=GOLD,width=3)
    T(d,(540,980),'Chame no WhatsApp',sans(40,'m'),WHITE,'ma'); T(d,(540,1040),'(44) 99884-6314',wide(68,900),WHITE,'ma'); T(d,(540,1150),'ou comente MIAMI',sans(40,'sb'),TAG,'ma')
    credit(s); s.save(OUT+'06-cta.jpg',quality=96)
    names=['01-miami-do-parana','02-4-mil-embarcacoes','03-por-do-sol','04-so-falta-o-seu','05-escolha-o-seu','06-cta']
    ims=[Image.open(OUT+n+'.jpg').resize((360,450)) for n in names]; c=Image.new('RGB',(370*6,450),'white')
    for i,im in enumerate(ims): c.paste(im,(i*370,0))
    c.save('/tmp/claude-0/miami_prev.jpg'); print('img ok')
if 'reel' in sys.argv:
    def kb(path,cx=0.5,cy=0.5,z0=1.0,z1=1.12,dx=0.0):
        im=Image.open(path).convert('RGB'); iw,ih=im.size
        def f(t,d_,txt=None):
            k=eio(seg(t,0,d_)); z=z0+(z1-z0)*k; ch=int(ih/z); cw=int(ch*9/16); x0=int(min(max(iw*(cx+dx*k)-cw/2,0),iw-cw)); y0=int(min(max(ih*cy-ch/2,0),ih-ch))
            return im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        return f
    LG=logo(320)
    def titled(base,l1,l2,y=300,s1=120,s2=84):
        def f(t,d_):
            fr=shade(base(t,d_),top=640,a1=200); fr=fr.convert('RGBA'); fr.alpha_composite(LG,(380,100)); dd=ImageDraw.Draw(fr); a=eo(seg(t,0.1,0.5))
            if a>0:
                dd.text((540,y),l1,font=wide(s1,900),fill=(255,255,255,int(255*a)),anchor='ma',stroke_width=5,stroke_fill=NAVY2)
                dd.text((540,y+s1+20),l2,font=wide(s2,900),fill=TAG+(int(255*a),),anchor='ma',stroke_width=5,stroke_fill=NAVY2)
            fr=fr.convert('RGB'); credit(fr); return fr
        return f
    city=kb(B+'protorico_cidade_foto_rdziura-2404.jpg',cx=0.55,cy=0.5,z0=1.0,z1=1.15,dx=0.1)
    prai=kb(B+'protorico_aereas_foto_rdziura-0109.jpg',cx=0.4,cy=0.5,z0=1.05,z1=1.2,dx=0.08)
    BGS=crop(B+'portorico_pordosol_foto_rdziura-1648.jpg',1240,2204,cx=0.2,cy=0.5)
    JS=rs(J170,820)
    def sunset(t,d_):
        z=1+0.06*t/d_; cw=int(1240/z*0.871); ch=int(cw*16/9); x0=(1240-cw)//2; y0=(2204-ch)//2
        b=BGS.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        real.place(b,JS,W-820+10,int(H*0.74-JS.height*0.82+7*math.sin(t*2)),wl=0.82,t=t,seed=4,gr=SUNSET); return b
    BGI=real.bg_crop('ilha_carioca_foto_rdzura-1754.jpg',1240,2204,cx_frac=0.52,cy_frac=0.5); JI=rs(J230,840)
    def ilha(t,d_):
        z=1+0.06*t/d_; cw=int(1240/z*0.871); ch=int(cw*16/9); x0=(1240-cw)//2; y0=(2204-ch)//2
        b=BGI.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        real.place(b,JI,W-840+10,int(H*0.72-JI.height*0.80+7*math.sin(t*2.1)),wl=0.80,t=t,seed=6); return b
    STU=kit.studio(W,H,cy=1000)
    def lineup(t,d_):
        n=len(JC); k=min(n-1,int(t/(d_/n))); J,m,a,h,p=JC[k]; lt=t-k*(d_/n)
        fr=STU.copy(); w_=int(min(900,900*760/(J.height*900/J.width))); j=rs(J,w_); kit.place_jet(fr,j,(W-w_)//2+int(40*(1-eo(seg(lt,0,0.25)))),640+(760-j.height)//2,refl=False)
        fr=fr.convert('RGBA'); fr.alpha_composite(LG,(380,100)); dd=ImageDraw.Draw(fr)
        dd.text((540,330),'ESCOLHA O SEU',font=sans(44,'b'),fill=TAG,anchor='ma')
        dd.text((540,400),f'Sea-Doo {m}',font=wide(84,900),fill=WHITE,anchor='ma'); dd.text((540,510),f'{a} · {h}',font=sans(46,'sb'),fill=MUTE,anchor='ma')
        dd.rounded_rectangle((290,1480,790,1580),radius=50,fill=TAG); dd.text((540,1530),p,font=wide(54,900),fill=NAVY2,anchor='mm')
        return fr.convert('RGB')
    def endcard(t,d_):
        b=shade(crop(B+'portorico_pordosol_foto_rdziura-0076.jpg',W,H,cx=0.5,cy=0.5),top=0,bot=1500,a2=235); e=eo(seg(t,0,0.4))
        L=logo(700); b.paste(L,(190,int(560-40*(1-e))),L); dr=ImageDraw.Draw(b)
        dr.text((540,860),'Seu lugar na Miami do Paraná',font=wide(48,900),fill=WHITE,anchor='mm'); dr.text((540,930),'começa aqui.',font=wide(48,900),fill=TAG,anchor='mm')
        dr.line((140,1010,940,1010),fill=GOLD,width=3)
        dr.text((540,1080),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((540,1160),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
        dr.text((540,1270),'ou comente MIAMI',font=sans(40,'sb'),fill=TAG,anchor='mm'); credit(b); return b
    sc=[dict(spk='Tem gente que chama de Miami do Paraná.',cap=None,draw=titled(city,'MIAMI','DO PARANÁ'),flash=False,min=3.0),
        dict(spk='Porto Rico tem mais de quatro mil embarcações registradas. É a cidade com mais barcos do estado.',cap='Porto Rico tem mais de 4 mil embarcações registradas. É a cidade com mais barcos do estado.',draw=titled(prai,'+4 MIL','EMBARCAÇÕES',s1=130),ycap=1560),
        dict(spk='O pôr do sol mais bonito do rio Paraná...',cap='O pôr do sol mais bonito do rio Paraná...',draw=titled(kb(B+'portorico_pordosol_foto_rdziura-0060.jpg',cx=0.5,z0=1.0,z1=1.12,dx=0.05),'PÔR DO SOL','QUE VALE A VIAGEM',s1=110,s2=60),ycap=1560),
        dict(spk='E a Prainha de Santa Rosa te esperando. Só falta o seu jet.',cap='E a Prainha de Santa Rosa te esperando. Só falta o seu jet.',draw=titled(kb(SRD+'praia_santa_rosa_foto_rdzura-0085.jpg',cx=0.55,z0=1.0,z1=1.15,dx=0.04),'PRAINHA DE','SANTA ROSA',s1=96,s2=110),ycap=1560),
        dict(spk='Na Cântri você escolhe o seu. Tem GTI e GTX, de cento e cinco a cento e quarenta e cinco mil.',cap='Na Country você escolhe o seu. Tem GTI e GTX, de R$ 105 a R$ 145 mil.',draw=lineup,ycap=1680,min=6.3),
        dict(spk='Seu lugar na Miami do Paraná começa na Cântri. Chama no zap!',cap=None,draw=endcard,min=4.0)]
    print('reel',build(sc,OUT+'reel-miami-do-parana.mp4'))
