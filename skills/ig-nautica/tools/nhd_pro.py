import sys; sys.path.insert(0,'.')
from nhd import *   # helpers: fit, tile, boat, enh, P, chip, T ...
OUT='/home/user/instagram-agent-skill/midia/aluguel-nhd280-pro/'
BG=(13,24,40); BG2=(19,33,54); LINE=(196,160,104); SOFT=(150,163,184)
W_,H_=1080,1350; M=72
def thin(size,w=300): return wide(size,w)
def kicker(d,x,y,t,fill=TAG,anchor='la'):
    f=sans(24,'sb'); sp=6; ws=[d.textlength(c,font=f) for c in t]; tot=sum(ws)+sp*(len(t)-1)
    x0=x-tot/2 if anchor=='ma' else x
    for c,w in zip(t,ws): d.text((x0,y),c,font=f,fill=fill); x0+=w+sp
def header(s,d,n,title,sub=None):
    L=logo(190); s.paste(L,(M,58),L); d.text((W_-M,72),f'0{n} / 07',font=sans(22,'m'),fill=SOFT,anchor='ra')
    d.line((M,140,W_-M,140),fill=(44,62,88),width=1)
    kicker(d,M,178,'ALUGUEL · NHD 280'); d.text((M-4,214),title,font=wide(64,800),fill=WHITE)
    if sub: d.text((M,300),sub,font=sans(30,'m'),fill=SOFT)
def footer(d,t='Reservas pelo WhatsApp  (44) 99884-6314'):
    d.line((M,H_-110,W_-M,H_-110),fill=(44,62,88),width=1); d.text((M,H_-78),t,font=sans(26,'m'),fill=SOFT)
def ph(name,w,h,cx=0.5,cy=0.5,zoom=1.0): return fit(P(name),w,h,cx=cx,cy=cy,zoom=zoom)
def label(s,x,y,w,t):
    d=ImageDraw.Draw(s); tw=d.textlength(t,font=sans(24,'sb'))
    ov=Image.new('RGBA',s.size,(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle((x,y,x+tw+36,y+46),radius=23,fill=BG+(215,)); s.paste(ov,(0,0),ov)
    ImageDraw.Draw(s).text((x+18,y+23),t,font=sans(24,'sb'),fill=WHITE,anchor='lm')
if 'pimg' in sys.argv:
    # 01 CAPA
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s)
    yy=np.linspace(0,1,H_)[:,None]; g=(np.array(BG2)*(1-yy)+np.array(BG)*yy); s=Image.fromarray(np.repeat(g[:,None,:],W_,1).astype('uint8')); d=ImageDraw.Draw(s)
    L=logo(220); s.paste(L,(M,64),L); d.text((W_-M,86),'Porto Rico · PR',font=sans(26,'m'),fill=SOFT,anchor='ra')
    kicker(d,540,250,'ALUGUEL DE LANCHA',anchor='ma'); d.text((540,300),'NHD 280',font=wide(150,900),fill=WHITE,anchor='ma')
    d.line((440,490,640,490),fill=LINE,width=2)
    d.text((540,520),'Seu dia no Rio Paraná, com conforto de verdade.',font=sans(32,'m'),fill=SOFT,anchor='ma')
    st=kit.studio(W_,640,cy=320,glow=0.6); kit.place_jet(st,boat(1000),W_-1000+20,150,refl=True); s.paste(st,(0,600)); d=ImageDraw.Draw(s)
    d.rectangle((0,600,W_,602),fill=BG)
    items=[('28','PÉS'),('280','HP'),('A/C','NA CABINE')]
    for i,(a_,b_) in enumerate(items):
        cx=180+i*360; d.text((cx,1150),a_,font=wide(52,800),fill=WHITE,anchor='ma'); d.text((cx,1222),b_,font=sans(22,'sb'),fill=TAG,anchor='ma')
        if i: d.line((cx-180,1150,cx-180,1250),fill=(44,62,88),width=1)
    s.save(OUT+'01-capa.jpg',quality=96)
    # 02 A BORDO (grade)
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,2,'A bordo','Tudo o que você precisa para o dia perfeito.')
    gw,gh,gap=(W_-2*M-24)//2,262,24; y0=380
    cells=[('bb2369bb',0.55,'Churrasqueira'),('819e42ac',0.42,'Som potente'),('ee557b53',0.5,'Cabine com mesa'),('494e31cb',0.45,'Ar-condicionado'),('550c4289',0.5,'Banheiro com ducha'),('06f7f0bf',0.42,'Sofá na popa')]
    for k,(n_,cy_,lb) in enumerate(cells):
        x=M+(k%2)*(gw+gap); y=y0+(k//2)*(gh+gap); tile(s,ph(n_,gw,gh,cy=cy_),x,y,r=18); label(s,x+16,y+gh-62,gw,lb)
    d=ImageDraw.Draw(s); footer(d); s.save(OUT+'02-a-bordo.jpg',quality=96)
    # 03 CHURRASCO (foto cheia)
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,3,'Churrasco a bordo','Churrasqueira, tábua e pia na popa.')
    tile(s,ph('bb2369bb',W_-2*M,800,cy=0.55),M,380,r=20); d=ImageDraw.Draw(s); footer(d); s.save(OUT+'03-churrasco.jpg',quality=96)
    # 04 CABINE
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,4,'Cabine climatizada','Para descansar, trocar de roupa ou fugir do sol.')
    tile(s,ph('ee557b53',560,800,cy=0.45),M,380,r=20)
    tile(s,ph('494e31cb',372,388,cy=0.45),M+584,380,r=20); tile(s,ph('550c4289',372,388,cy=0.5),M+584,792,r=20)
    d=ImageDraw.Draw(s); footer(d); s.save(OUT+'04-cabine.jpg',quality=96)
    # 05 SOM + ESPAÇO
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,5,'Som e espaço','Caixas na torre, subwoofer e bancos para a turma.')
    tile(s,ph('819e42ac',460,800,cy=0.42),M,380,r=20)
    tile(s,ph('0dcbd92a',472,388,cy=0.28,zoom=1.5),M+484,380,r=20); tile(s,ph('06f7f0bf',472,388,cy=0.42),M+484,792,r=20)
    d=ImageDraw.Draw(s); footer(d); s.save(OUT+'05-som-espaco.jpg',quality=96)
    # 06 FICHA
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,6,'Ficha da lancha')
    st=kit.studio(W_,330,cy=160,glow=0.5); kit.place_jet(st,boat(760),(W_-760)//2,70,refl=False); s.paste(st,(0,320)); d=ImageDraw.Draw(s)
    rows=[('Modelo','NHD 280'),('Comprimento','28 pés (8,4 m)'),('Motor','280 hp'),('Cabine','Mesa e ar-condicionado'),('Banheiro','Pia e ducha'),('Lazer','Churrasqueira, som, toldo'),('Banho','Plataforma com escada')]
    y=690
    for k_,v_ in rows:
        d.text((M,y),k_,font=sans(30,'m'),fill=SOFT); d.text((W_-M,y),v_,font=sans(32,'sb'),fill=WHITE,anchor='ra'); y+=66; d.line((M,y-14,W_-M,y-14),fill=(38,55,80),width=1)
    footer(d); s.save(OUT+'06-ficha.jpg',quality=96)
    # 07 RESERVA
    s=Image.new('RGB',(W_,H_),BG); d=ImageDraw.Draw(s); header(s,d,7,'Como reservar')
    steps=[('1','Escolha a data','Dia inteiro ou meio período.'),('2','Chame no WhatsApp','Tiramos suas dúvidas e enviamos os valores.'),('3','Confirme a reserva','Sua data fica garantida.')]
    y=380
    for n_,t1,t2 in steps:
        d.rounded_rectangle((M,y,W_-M,y+170),radius=22,fill=BG2,outline=(44,62,88),width=1)
        d.ellipse((M+36,y+45,M+116,y+125),outline=LINE,width=3); d.text((M+76,y+85),n_,font=wide(40,800),fill=TAG,anchor='mm')
        d.text((M+150,y+40),t1,font=wide(40,800),fill=WHITE); d.text((M+152,y+100),t2,font=sans(28,'m'),fill=SOFT); y+=200
    d.text((540,1010),'(44) 99884-6314',font=wide(66,900),fill=WHITE,anchor='ma'); d.text((540,1100),'ou comente LANCHA',font=sans(32,'sb'),fill=TAG,anchor='ma')
    L=logo(230); s.paste(L,(425,1190),L); s.save(OUT+'07-reserva.jpg',quality=96)
    # STORY
    st=Image.new('RGB',(1080,1920),BG); d=ImageDraw.Draw(st); L=logo(260); st.paste(L,(410,110),L)
    kicker(d,540,330,'ALUGUEL DE LANCHA',anchor='ma'); d.text((540,380),'NHD 280',font=wide(140,900),fill=WHITE,anchor='ma')
    s2=kit.studio(1080,560,cy=280,glow=0.6); kit.place_jet(s2,boat(1000),60,170,refl=True); st.paste(s2,(0,600)); d=ImageDraw.Draw(st)
    for i,(n_,lb) in enumerate([('bb2369bb','Churrasqueira'),('ee557b53','Cabine com ar'),('819e42ac','Som')]):
        x=60+i*330; tile(st,ph(n_,300,300,cy=0.5),x,1220,r=18); d=ImageDraw.Draw(st); d.text((x+150,1540),lb,font=sans(28,'sb'),fill=WHITE,anchor='ma')
    d.rounded_rectangle((140,1680,940,1780),radius=50,fill=TAG); d.text((540,1730),'Reserve sua data',font=wide(40,900),fill=NAVY2,anchor='mm')
    d.text((540,1830),'[ cole o link do WhatsApp aqui ]',font=sans(26,'m'),fill=SOFT,anchor='ma')
    st.save(OUT+'story.jpg',quality=96)
    names=['01-capa','02-a-bordo','03-churrasco','04-cabine','05-som-espaco','06-ficha','07-reserva']
    ims=[Image.open(OUT+n+'.jpg').resize((324,405)) for n in names]+[Image.open(OUT+'story.jpg').resize((228,405))]
    c=Image.new('RGB',(334*7+238,405),'white'); x=0
    for im in ims: c.paste(im,(x,0)); x+=im.width+10
    c.save('/tmp/claude-0/pro_prev.jpg'); print('pro img ok')
if 'preel' in sys.argv:
    LGv=logo(260)
    def bgv():
        yy=np.linspace(0,1,H)[:,None]; g=(np.array(BG2)*(1-yy)+np.array(BG)*yy); return Image.fromarray(np.repeat(g[:,None,:],W,1).astype('uint8'))
    BGV=bgv()
    def opener(t,d_):
        fr=BGV.copy(); d=ImageDraw.Draw(fr); fr.paste(LGv,(410,110),LGv); a=eo(seg(t,0.1,0.6))
        kicker(d,540,420,'ALUGUEL DE LANCHA',anchor='ma'); d.text((540,470),'NHD 280',font=wide(150,900),fill=WHITE,anchor='ma')
        st=kit.studio(W,640,cy=320,glow=0.6); bw=1000; kit.place_jet(st,boat(bw),W-bw+20+int(260*(1-eo(seg(t,0,1.0)))),160,refl=True); fr.paste(st,(0,760))
        d=ImageDraw.Draw(fr)
        for i,(a_,b_) in enumerate([('28','PÉS'),('280','HP'),('A/C','NA CABINE')]):
            cx=180+i*360; d.text((cx,1460),a_,font=wide(56,800),fill=WHITE,anchor='ma'); d.text((cx,1535),b_,font=sans(24,'sb'),fill=TAG,anchor='ma')
        return fr
    def photo(name,cy,title,zoom=1.0):
        im=enh(Image.open(P(name)).convert('RGB')); iw,ih=im.size
        def f(t,d_):
            z=zoom+0.08*eio(seg(t,0,d_)); ch=int(ih/z); cw=int(ch*9/16)
            if cw>iw: cw=iw; ch=int(cw*16/9)
            x0=(iw-cw)//2; y0=int(min(max(ih*cy-ch/2,0),ih-ch))
            fr=im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS).convert('RGBA')
            ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
            for y in range(380): od.line((0,y,W,y),fill=BG+(int(200*(1-y/380)),))
            fr.alpha_composite(ov); fr.alpha_composite(LGv,(410,90)); d=ImageDraw.Draw(fr); a=int(255*eo(seg(t,0,0.35)))
            d.text((540,250),title,font=wide(64,800),fill=(255,255,255,a),anchor='ma',stroke_width=3,stroke_fill=BG)
            d.line((470,340,610,340),fill=LINE+(a,),width=2)
            return fr.convert('RGB')
        return f
    def ficha(t,d_):
        fr=BGV.copy(); d=ImageDraw.Draw(fr); fr.paste(LGv,(410,110),LGv); kicker(d,540,330,'FICHA DA LANCHA',anchor='ma')
        rows=[('Comprimento','28 pés'),('Motor','280 hp'),('Cabine','Mesa e ar'),('Banheiro','Pia e ducha'),('Lazer','Churrasqueira e som')]
        y=440
        for k,(a_,b_) in enumerate(rows):
            al=eo(seg(t,0.15*k,0.15*k+0.35))
            if al<=0: break
            d.text((M+int(40*(1-al)),y),a_,font=sans(36,'m'),fill=SOFT); d.text((W-M,y),b_,font=sans(38,'sb'),fill=WHITE,anchor='ra'); y+=90; d.line((M,y-22,W-M,y-22),fill=(38,55,80),width=1)
        return fr
    def end(t,d_):
        fr=BGV.copy(); d=ImageDraw.Draw(fr); e=eo(seg(t,0,0.4)); L=logo(620); fr.paste(L,(230,int(560-30*(1-e))),L)
        d.text((540,860),'Reserve sua data',font=wide(70,900),fill=WHITE,anchor='mm'); d.line((440,940,640,940),fill=LINE,width=2)
        d.text((540,1010),'Chame no WhatsApp',font=sans(40,'m'),fill=SOFT,anchor='mm'); d.text((540,1090),'(44) 99884-6314',font=wide(70,900),fill=WHITE,anchor='mm')
        d.text((540,1200),'ou comente LANCHA',font=sans(38,'sb'),fill=TAG,anchor='mm'); return fr
    sc=[dict(spk='Alugue a lancha NHD 280, aqui em Porto Rico.',cap=None,draw=opener,flash=False,min=3.2),
        dict(spk='Churrasqueira a bordo, com tábua e pia.',cap='Churrasqueira a bordo, com tábua e pia.',draw=photo('bb2369bb',0.55,'Churrasqueira'),ycap=1600),
        dict(spk='Cabine com mesa e ar-condicionado.',cap='Cabine com mesa e ar-condicionado.',draw=photo('ee557b53',0.5,'Cabine climatizada'),ycap=1600),
        dict(spk='Banheiro com pia e ducha.',cap='Banheiro com pia e ducha.',draw=photo('550c4289',0.5,'Banheiro'),ycap=1600),
        dict(spk='Som potente, pra animar o dia.',cap='Som potente, pra animar o dia.',draw=photo('819e42ac',0.45,'Som'),ycap=1600),
        dict(spk='E espaço pra turma toda.',cap='E espaço pra turma toda.',draw=photo('0dcbd92a',0.3,'Espaço',zoom=1.55),ycap=1600),
        dict(spk='Vinte e oito pés, motor de duzentos e oitenta cavalos.',cap='28 pés, motor de 280 cavalos.',draw=ficha,flash=False,ycap=1600,min=3.4),
        dict(spk='Reserve sua data. Chama a Cântri no zap!',cap=None,draw=end,min=3.4)]
    print('reel',build(sc,OUT+'reel-aluguel-nhd280.mp4'))
