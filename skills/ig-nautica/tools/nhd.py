import sys; sys.path.insert(0,'.')
from motor import *
import kit
U='/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/'; B='/tmp/claude-0/aen/b/'; SRD='/tmp/claude-0/aen/sr/'
OUT='/home/user/instagram-agent-skill/midia/aluguel-nhd280/'
def P(n): return U+n+'-image.jpg'
def enh(im,b=1.08,c=1.12,s=1.15,warm=True):
    im=ImageEnhance.Brightness(im).enhance(b); im=ImageEnhance.Contrast(im).enhance(c); im=ImageEnhance.Color(im).enhance(s)
    if warm:
        a=np.array(im).astype(float); a*=np.array([1.04,1.0,0.95]); im=Image.fromarray(np.clip(a,0,255).astype('uint8'))
    return im.filter(ImageFilter.UnsharpMask(2,50,2))
def fit(path,w,h,cx=0.5,cy=0.5,zoom=1.0,e=True):
    im=Image.open(path).convert('RGB'); iw,ih=im.size; r=w/h; ch=int(ih/zoom); cw=int(ch*r)
    if cw>iw/zoom: cw=int(iw/zoom); ch=int(cw/r)
    x0=int(min(max(iw*cx-cw/2,0),iw-cw)); y0=int(min(max(ih*cy-ch/2,0),ih-ch))
    im=im.crop((x0,y0,x0+cw,y0+ch)).resize((w,h),Image.LANCZOS); return enh(im) if e else im
def tile(s,im,x,y,r=28):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.width-1,im.height-1),radius=r,fill=255); s.paste(im,(x,y),m)
def shade(im,top=0,bot=0,a1=190,a2=200):
    im=im.convert('RGBA'); W_,H_=im.size; ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top): d.line((0,y,W_,y),fill=NAVY2+(int(a1*(1-y/top)),))
    for y in range(bot): d.line((0,H_-1-y,W_,H_-1-y),fill=NAVY2+(int(a2*(1-y/bot)),))
    im.alpha_composite(ov); return im.convert('RGB')
def T(d,xy,t,f,fill,anchor='la',sw=0): d.text(xy,t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=NAVY2)
def chip(d,x,y,t,bg=TAG,fg=NAVY2,f=None):
    f=f or sans(30,'b'); w=d.textlength(t,font=f); d.rounded_rectangle((x,y,x+w+48,y+58),radius=29,fill=bg); d.text((x+24,y+29),t,font=f,fill=fg,anchor='lm'); return w+48
CRED='Cenários de Porto Rico: Roberto Dziura Jr./AEN (domínio público)'
def cred(s): ImageDraw.Draw(s).text((s.width/2,s.height-20),CRED,font=sans(16,'m'),fill=(225,230,235),anchor='mm')
# lancha recortada (sem carreta)
BO=Image.open('/tmp/claude-0/nhd_0c47aa73.png').convert('RGBA'); BO=BO.crop(BO.getbbox())
a=np.array(BO).astype(float); h=a.shape[0]; yy=np.arange(h)[:,None]; c0,c1=int(h*0.60),int(h*0.70); a[...,3]*=np.clip((c1-yy)/(c1-c0),0,1); BO=Image.fromarray(a.astype('uint8'),'RGBA').crop((0,0,BO.width,c1))
BO=ImageEnhance.Contrast(BO).enhance(1.1)
def boat(w): return BO.resize((w,int(BO.height*w/BO.width)),Image.LANCZOS)
W_,H_=1080,1350
def foot(s,d,n,dark=True):
    L=logo(220); s.paste(L,(60,H_-100),L); d.text((W_-60,H_-62),f'{n}/8',font=sans(26,'m'),fill=MUTE,anchor='ra')
if 'img' in sys.argv:
    # 1 CAPA
    s=Image.new('RGB',(W_,H_),NAVY)
    top=shade(fit(SRD+'praia_santa_rosa_foto_rdzura-0085.jpg',W_,700,cx=0.52,cy=0.45,e=False),top=420,a1=215); s.paste(top,(0,0)); d=ImageDraw.Draw(s)
    L=logo(250); s.paste(L,(60,50),L)
    T(d,(60,150),'ALUGUE UMA',wide(64,900),WHITE,sw=3); T(d,(56,225),'LANCHA',wide(150,900),TAG,sw=3); T(d,(62,400),'na Miami do Paraná',wide(50,850),WHITE,sw=3)
    st=kit.studio(W_,H_-700,cy=330); bw=960; kit.place_jet(st,boat(bw),W_-bw+12,190,refl=True); s.paste(st,(0,700)); d=ImageDraw.Draw(s)
    d.rectangle((0,694,W_,702),fill=TAG)
    T(d,(60,740),'NHD 280',wide(76,900),WHITE); d.text((62,840),'28 pés · cabine · churrasqueira',font=sans(34,'sb'),fill=MUTE)
    chip(d,60,1180,'Reserve sua data',f=wide(34,900)); d.text((1020,1209),'(44) 99884-6314',font=wide(36,850),fill=WHITE,anchor='rm')
    cred(s); s.save(OUT+'01-capa.jpg',quality=96)
    # 2 CHURRASCO
    s=Image.new('RGB',(W_,H_),NAVY); tile(s,fit(P('bb2369bb'),960,900,cx=0.5,cy=0.55),60,330); d=ImageDraw.Draw(s)
    T(d,(60,70),'Churrasco',wide(96,900),WHITE); T(d,(60,180),'a bordo. 🔥'.replace(' 🔥',''),wide(96,900),TAG)
    chip(d,80,1150,'Churrasqueira',f=sans(30,'b')); x=80+d.textlength('Churrasqueira',font=sans(30,'b'))+60; x+=chip(d,x,1150,'Tábua',f=sans(30,'b'))+12; chip(d,x,1150,'Pia',f=sans(30,'b'))
    foot(s,d,2); s.save(OUT+'02-churrasco.jpg',quality=96)
    # 3 SOM
    s=Image.new('RGB',(W_,H_),NAVY2); d=ImageDraw.Draw(s)
    T(d,(60,70),'O som',wide(96,900),WHITE); T(d,(60,180),'da festa.',wide(96,900),TAG)
    tile(s,fit(P('819e42ac'),465,800,cy=0.45),60,330); tile(s,fit(P('4b34965f'),465,800,cy=0.5),555,330)
    d=ImageDraw.Draw(s); d.text((60,1140),'Caixas na torre, alto-falantes nas laterais',font=sans(34,'sb'),fill=WHITE); d.text((60,1185),'e subwoofer. Leve sua playlist.',font=sans(34,'sb'),fill=MUTE)
    foot(s,d,3); s.save(OUT+'03-som.jpg',quality=96)
    # 4 CABINE
    s=Image.new('RGB',(W_,H_),NAVY); d=ImageDraw.Draw(s)
    T(d,(60,70),'Cabine com',wide(80,900),WHITE); T(d,(60,165),'ar-condicionado.',wide(80,900),TAG)
    tile(s,fit(P('ee557b53'),600,800,cy=0.45),60,290); tile(s,fit(P('494e31cb'),340,390,cy=0.45),680,290); tile(s,fit(P('550c4289'),340,390,cy=0.5),680,700)
    d=ImageDraw.Draw(s); x=60; 
    for t_ in ['Ar-condicionado','Banheiro com ducha','Mesa']: x+=chip(d,x,1130,t_,f=sans(28,'b'))+12
    foot(s,d,4); s.save(OUT+'04-cabine.jpg',quality=96)
    # 5 ESPAÇO
    s=Image.new('RGB',(W_,H_),NAVY2); d=ImageDraw.Draw(s)
    T(d,(60,70),'Espaço pra',wide(84,900),WHITE); T(d,(60,170),'turma toda.',wide(84,900),TAG)
    tile(s,fit(P('0dcbd92a'),465,820,cy=0.30,zoom=1.35),60,300); tile(s,fit(P('06f7f0bf'),465,395,cy=0.4),555,300); tile(s,fit(P('280e20c2'),465,395,cy=0.62),555,725)
    d=ImageDraw.Draw(s); d.text((60,1135),'Bancos em toda a volta, toldo para a sombra,',font=sans(32,'sb'),fill=WHITE); d.text((60,1180),'pia, porta-copos e escada para pular no rio.',font=sans(32,'sb'),fill=MUTE)
    foot(s,d,5); s.save(OUT+'05-espaco.jpg',quality=96)
    # 5b BEM CUIDADA
    s=Image.new('RGB',(W_,H_),NAVY); d=ImageDraw.Draw(s)
    T(d,(60,70),'Lancha',wide(90,900),WHITE); T(d,(60,175),'bem cuidada.',wide(90,900),TAG)
    tile(s,fit(P('75410d9f'),465,560,cy=0.4),60,320); tile(s,fit(P('83ddd2e8'),465,560,cy=0.45),555,320)
    tile(s,fit(P('890a70f7'),960,200,cy=0.50,zoom=1.0),60,900); d=ImageDraw.Draw(s)
    x=60
    for t_ in ['Só 68 h de motor','MerCruiser 250 hp','Bússola e âncora elétrica']: x+=chip(d,x,1125,t_,f=sans(26,'b'))+10
    foot(s,d,6); s.save(OUT+'05b-bem-cuidada.jpg',quality=96)
    # 6 ROTEIROS
    s=Image.new('RGB',(W_,H_),NAVY); d=ImageDraw.Draw(s)
    T(d,(60,60),'Escolha o passeio',wide(70,900),WHITE)
    for i,(img,cy_,t1,t2) in enumerate([(SRD+'praia_santa_rosa_foto_rdzura-0085.jpg',0.5,'Dia na prainha','Prainha de Santa Rosa'),(B+'portorico_pordosol_foto_rdziura-0060.jpg',0.55,'Pôr do sol','no Rio Paraná')]):
        y=180+i*510; im=shade(fit(img,960,480,cy=cy_,e=False),bot=260,a2=210); tile(s,im,60,y); d=ImageDraw.Draw(s)
        T(d,(100,y+330),t1,wide(60,900),WHITE); d.text((102,y+410),t2,font=sans(32,'sb'),fill=TAG)
    d.text((60,1195),'Aniversário, família, amigos ou casal.',font=sans(30,'sb'),fill=MUTE)
    foot(s,d,7); cred(s); s.save(OUT+'06-roteiros.jpg',quality=96)
    # 7 CTA (foto real em cima, lancha em estúdio embaixo)
    s=Image.new('RGB',(W_,H_),NAVY)
    top=shade(fit(B+'portorico_pordosol_foto_rdziura-0076.jpg',W_,560,cy=0.45,e=False),top=360,a1=200); s.paste(top,(0,0)); d=ImageDraw.Draw(s)
    T(d,(540,90),'Reserve sua data',wide(80,900),WHITE,'ma',sw=4); T(d,(540,195),'na NHD 280',wide(60,900),TAG,'ma',sw=4)
    d.rectangle((0,556,W_,564),fill=TAG)
    st=kit.studio(W_,H_-564,cy=200); bw=900; kit.place_jet(st,boat(bw),W_-bw+12,40,refl=True); s.paste(st,(0,564)); d=ImageDraw.Draw(s)
    T(d,(540,920),'O verão em Porto Rico lota rápido.',sans(36,'sb'),WHITE,'ma'); T(d,(540,985),'Chame no WhatsApp',sans(38,'m'),MUTE,'ma')
    T(d,(540,1040),'(44) 99884-6314',wide(68,900),WHITE,'ma'); T(d,(540,1140),'ou comente LANCHA',sans(38,'sb'),TAG,'ma')
    L=logo(240); s.paste(L,(420,1215),L); cred(s); s.save(OUT+'07-reserve.jpg',quality=96)
    # STORY enquete
    st=Image.new('RGB',(1080,1920),NAVY2); d=ImageDraw.Draw(st); L=logo(300); st.paste(L,(390,90),L)
    T(d,(540,240),'Qual passeio de lancha',wide(58,900),WHITE,'ma'); T(d,(540,320),'você faria?',wide(58,900),TAG,'ma')
    tile(st,shade(fit(SRD+'praia_santa_rosa_foto_rdzura-0085.jpg',960,620,e=False),bot=200,a2=200),60,440); tile(st,shade(fit(B+'portorico_pordosol_foto_rdziura-0060.jpg',960,620,e=False),bot=200,a2=200),60,1090)
    d=ImageDraw.Draw(st); T(d,(100,980),'Dia na prainha',wide(52,900),WHITE); T(d,(100,1630),'Pôr do sol no rio',wide(52,900),WHITE)
    d.rounded_rectangle((240,1750,840,1850),radius=30,outline=TAG,width=3); d.text((540,1800),'[ figurinha ENQUETE aqui ]',font=sans(28,'m'),fill=MUTE,anchor='mm')
    st.save(OUT+'story-enquete.jpg',quality=96)
    names=['01-capa','02-churrasco','03-som','04-cabine','05-espaco','05b-bem-cuidada','06-roteiros','07-reserve']
    ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story-enquete.jpg').resize((228,405))]
    c=Image.new('RGB',(334*8+238,405),'white'); x=0
    for im in ims: c.paste(im,(x,0)); x+=im.width+10
    c.save('/tmp/claude-0/nhd_prev.jpg'); print('img ok')
if 'reel' in sys.argv:
    LG=logo(300)
    def kb(path,cx=0.5,cy=0.5,z0=1.0,z1=1.12,dx=0.0,e=True):
        im=Image.open(path).convert('RGB'); im=enh(im) if e else im; iw,ih=im.size
        def f(t,d_):
            k=eio(seg(t,0,d_)); z=z0+(z1-z0)*k; ch=int(ih/z); cw=int(ch*9/16)
            if cw>iw: cw=iw; ch=int(cw*16/9)
            x0=int(min(max(iw*(cx+dx*k)-cw/2,0),iw-cw)); y0=int(min(max(ih*cy-ch/2,0),ih-ch))
            return im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        return f
    def titled(base,l1,l2,s1=96,s2=80,credit=False):
        def f(t,d_):
            fr=shade(base(t,d_),top=640,a1=205).convert('RGBA'); fr.alpha_composite(LG,(390,90)); dd=ImageDraw.Draw(fr); a=eo(seg(t,0.05,0.4))
            dd.text((540,270),l1,font=wide(s1,900),fill=(255,255,255,int(255*a)),anchor='ma',stroke_width=5,stroke_fill=NAVY2)
            dd.text((540,270+s1+16),l2,font=wide(s2,900),fill=TAG+(int(255*a),),anchor='ma',stroke_width=5,stroke_fill=NAVY2)
            fr=fr.convert('RGB')
            if credit: cred(fr)
            return fr
        return f
    STU=kit.studio(W,H,cy=1000)
    def boatsc(t,d_):
        fr=STU.copy(); r_=eo(seg(t,0,0.9)); bw=int(1000*(0.9+0.1*r_)); b=boat(bw)
        kit.place_jet(fr,b,W-bw+12+int(300*(1-r_)),820,refl=True)
        fr=fr.convert('RGBA'); fr.alpha_composite(LG,(390,90)); dd=ImageDraw.Draw(fr); a=eo(seg(t,0.3,0.7))
        dd.text((540,300),'NHD 280',font=wide(130,900),fill=(255,255,255,int(255*a)),anchor='ma')
        dd.text((540,460),'28 pés · motor 250 hp',font=sans(50,'sb'),fill=TAG+(int(255*a),),anchor='ma')
        return fr.convert('RGB')
    def endcard(t,d_):
        b=shade(fit(B+'portorico_pordosol_foto_rdziura-0076.jpg',W,H,e=False),top=0,bot=1500,a2=235); e=eo(seg(t,0,0.4))
        L=logo(700); b.paste(L,(190,int(520-40*(1-e))),L); dr=ImageDraw.Draw(b)
        dr.text((540,840),'Reserve sua data',font=wide(70,900),fill=WHITE,anchor='mm'); dr.text((540,930),'na NHD 280',font=wide(52,900),fill=TAG,anchor='mm')
        dr.line((140,1010,940,1010),fill=GOLD,width=3)
        dr.text((540,1080),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((540,1160),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
        dr.text((540,1270),'ou comente LANCHA',font=sans(40,'sb'),fill=TAG,anchor='mm'); cred(b); return b
    sc=[dict(spk='Bora passar o dia na Prainha de Santa Rosa... de lancha?',cap=None,draw=titled(kb(SRD+'praia_santa_rosa_foto_rdzura-0085.jpg',cx=0.55,z0=1.0,z1=1.15,dx=0.04,e=False),'ALUGUE UMA','LANCHA',s1=90,s2=140,credit=True),flash=False,min=3.0),
     dict(spk='A nossa NHD 280 tem vinte e oito pés, e motor de duzentos e cinquenta cavalos.',cap='A nossa NHD 280 tem 28 pés, e motor de 250 cavalos.',draw=boatsc,ycap=1580),
     dict(spk='Churrasqueira a bordo, com tábua e pia.',cap='Churrasqueira a bordo, com tábua e pia.',draw=titled(kb(P('bb2369bb'),cy=0.55,z0=1.0,z1=1.1),'CHURRASCO','A BORDO',s1=100,s2=86),ycap=1580),
     dict(spk='Som de festa, com caixas na torre e subwoofer.',cap='Som de festa, com caixas na torre e subwoofer.',draw=titled(kb(P('819e42ac'),cy=0.45,z0=1.0,z1=1.1),'SOM DE','FESTA',s1=100,s2=120),ycap=1580),
     dict(spk='Cabine com ar-condicionado, e banheiro com ducha.',cap='Cabine com ar-condicionado, e banheiro com ducha.',draw=titled(kb(P('ee557b53'),cy=0.5,z0=1.0,z1=1.1),'CABINE','COM AR',s1=110,s2=110),ycap=1580),
     dict(spk='Espaço pra turma toda, e escada pra pular no rio.',cap='Espaço pra turma toda, e escada pra pular no rio.',draw=titled(kb(P('0dcbd92a'),cy=0.3,z0=1.55,z1=1.65),'ESPAÇO PRA','TURMA TODA',s1=90,s2=90),ycap=1580),
     dict(spk='Lancha bem cuidada, com só sessenta e oito horas de motor.',cap='Lancha bem cuidada, com só 68 horas de motor.',draw=titled(kb(P('75410d9f'),cy=0.45,z0=1.0,z1=1.12),'BEM','CUIDADA',s1=120,s2=120),ycap=1580),
     dict(spk='E pra fechar, o pôr do sol no rio Paraná.',cap='E pra fechar, o pôr do sol no rio Paraná.',draw=titled(kb(B+'portorico_pordosol_foto_rdziura-0060.jpg',cx=0.5,z0=1.0,z1=1.12,dx=0.05,e=False),'PÔR DO SOL','NO RIO PARANÁ',s1=100,s2=70,credit=True),ycap=1580),
     dict(spk='Reserve sua data. Chama a Cântri no zap!',cap=None,draw=endcard,min=3.6)]
    print('reel',build(sc,OUT+'reel-aluguel-nhd280.mp4'))
