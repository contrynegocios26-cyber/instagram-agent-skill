# Gerador completo de uma unidade: fotos -> carrossel, quadrado, stories e 3 Reels narrados
import sys,json,os; sys.path.insert(0,'.')
from motor import *
import kit
C=json.load(open(sys.argv[1])); OUT=C['out']; os.makedirs(OUT,exist_ok=True)
ONLY=sys.argv[2] if len(sys.argv)>2 else 'all'
# ---------- preparar jet e fundo ----------
cut=Image.open(C['cut']).convert('RGBA'); bb=cut.getbbox(); J=cut.crop(bb)
src=Image.open(C['foto']).convert('RGB')
jw=C.get('portrait_w',960); sc=jw/J.width; Jp=J.resize((jw,int(J.height*sc)),Image.LANCZOS)
bg=src.copy(); r=max(1080/bg.width,1920/bg.height); bg=bg.resize((int(bg.width*r),int(bg.height*r)),Image.LANCZOS)
bg=bg.crop(((bg.width-1080)//2,(bg.height-1920)//2,(bg.width-1080)//2+1080,(bg.height-1920)//2+1920))
bg=bg.filter(ImageFilter.GaussianBlur(C.get('blur',36))); bg=ImageEnhance.Brightness(bg).enhance(0.85)
jx=-12 if C.get('jet_left') else (1080-jw)//2; jy=C.get('portrait_y',250)
if C.get('portrait_cut'):
    ap=np.array(Jp).astype(float); hp_=ap.shape[0]; co=int(hp_*C['portrait_cut']); ap[...,3]*=np.clip((co-np.arange(hp_))/(hp_*0.06),0,1)[:,None]; Jp=Image.fromarray(ap.astype('uint8'),'RGBA')
sh=Image.new('L',(1080,1920),0); ImageDraw.Draw(sh).ellipse((jx+jw*0.1,jy+Jp.height*0.85,jx+jw*0.9,jy+Jp.height*1.02),fill=150); sh=sh.filter(ImageFilter.GaussianBlur(30)); bg.paste((0,0,0),(0,0),sh)
bg.paste(Jp,(jx,jy),Jp); bg=ImageEnhance.Contrast(bg).enhance(1.1); bg=ImageEnhance.Color(bg).enhance(1.12); P=bg.filter(ImageFilter.UnsharpMask(2,60,2))
a=np.array(J.resize((800,int(J.height*800/J.width)),Image.LANCZOS)).astype(float); hh=a.shape[0]; cutoff=int(hh*C.get('studio_cut',0.94))
a[...,3]*=np.clip((cutoff-np.arange(hh))/(hh*0.12),0,1)[:,None]
SJ=Image.fromarray(a.astype('uint8'),'RGBA').crop((0,0,800,cutoff)); SJ=ImageEnhance.Contrast(SJ).enhance(1.08); SJ=ImageEnhance.Brightness(SJ).enhance(C.get('studio_bright',1.0))
def sj(w): return SJ.resize((w,int(SJ.height*w/SJ.width)),Image.LANCZOS)
def XL(x): return -12 if C.get('jet_left') else x
COLS=[tuple(x) for x in C['cols']]; MOD=C['modelo']; MAR=C['marca']
W_,H_=1080,1350
def base(ct,panel,h=H_):
    ph=P.crop((0,ct,1080,ct+h)); fade_to_navy(ph,panel-200,panel); return ph
def num(d,i,n=7): d.text((W_-96,H_-60),f'{i}/{n}',font=sans(26,'m'),fill=MUTE)
def gold_big(s,text,y,size=330):
    mk=Image.new('L',s.size,0); ImageDraw.Draw(mk).text((s.width/2,y),text,font=wide(size,900),fill=255,anchor='ma')
    b=mk.getbbox(); gy=np.clip((np.arange(s.height)-b[1])/(b[3]-b[1]),0,1)[:,None,None]
    arr=np.repeat(np.array((236,205,150))*(1-gy)+np.array((160,118,62))*gy,s.width,1).astype('uint8'); s.paste(Image.fromarray(arr,'RGB'),(0,0),mk)
TAGSUB=C.get('tag_sub','modelo '+C['ano'])
if ONLY in('all','img'):
    s=base(300,880); d=ImageDraw.Draw(s)
    d.text((72,905),MAR,font=sans(40,'sb'),fill=GOLD); d.text((68,962),MOD,font=wide(C.get('model_size',104),850),fill=WHITE)
    d.line((72,1100,1008,1100),fill=GOLD,width=3); info_cols(d,1120,COLS); footer(s,d,1238)
    t=tag(C['preco'],TAGSUB,w=390,angle=6); s.paste(t,(495,650),t); s.save(OUT+'01-capa.jpg',quality=95)
    s=base(130,1000); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
    d.text((66,1015),f"{C['horas']} horas",font=wide(C.get('horas_size',150),850),fill=WHITE)
    d.text((72,1185),C['horas_l1'],font=sans(42,'sb'),fill=WHITE); d.text((72,1240),C['horas_l2'],font=sans(32,'m'),fill=MUTE)
    d.text((72,1290),'Arraste para conhecer →',font=sans(28,'sb'),fill=GOLD); s.save(OUT+'02-horas.jpg',quality=95)
    s=kit.studio(W_,H_,cy=760); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
    gold_big(s,C['hp'],190); d.text((W_/2,520),'CAVALOS',font=wide(56,850),fill=WHITE,anchor='ma')
    kit.place_jet(s,sj(760),XL(160),600); ov=Image.new('RGBA',(W_,H_),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for i in range(280): od.line((0,H_-280+i,W_,H_-280+i),fill=NAVY+(int(240*i/280),))
    s.paste(ov,(0,0),ov); d=ImageDraw.Draw(s)
    d.text((72,1150),C['motor_l1'],font=wide(42,800),fill=WHITE); d.text((72,1210),C['motor_l2'],font=sans(34,'m'),fill=MUTE); num(d,3); s.save(OUT+'03-motor.jpg',quality=95)
    s=Image.new('RGB',(W_,H_),NAVY); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
    d.text((72,200),'O que ele tem',font=sans(40,'sb'),fill=GOLD); d.text((68,250),C.get('feat_title','Equipado de fábrica'),font=wide(64,850),fill=WHITE)
    y=400
    for k,v in C['feats']:
        d.rounded_rectangle((72,y,1008,y+84),radius=18,fill=(30,50,77)); d.text((100,y+20),k,font=wide(32,850),fill=TAG); d.text((440,y+24),v,font=sans(32,'m'),fill=WHITE); y+=96
    d.text((72,1190),C['feat_note'],font=sans(24,'m'),fill=(130,145,165)); num(d,4); s.save(OUT+'04-equipamentos.jpg',quality=95)
    s=kit.studio(W_,H_,cy=700); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
    d.text((72,190),f'Conheça o {MOD}',font=wide(60,850),fill=WHITE)
    jw2=760; jx2,jy2=XL(40),420; kit.place_jet(s,sj(jw2),jx2,jy2); d=ImageDraw.Draw(s); k2=jw2/800
    for (px,py,ty,t1,t2) in C['callouts']:
        X,Y=jx2+px*k2,jy2+py*k2; tx=820
        d.ellipse((X-10,Y-10,X+10,Y+10),fill=TAG); d.ellipse((X-21,Y-21,X+21,Y+21),outline=TAG,width=3)
        d.line((X,Y,tx,ty),fill=TAG,width=3); d.line((tx,ty,1030,ty),fill=TAG,width=3)
        d.text((830,ty-58),t1,font=wide(42,850),fill=WHITE); d.text((830,ty+10),t2,font=sans(28,'m'),fill=MUTE)
    d.text((72,1190),C['detalhe_rodape'],font=sans(34,'sb'),fill=TAG); num(d,5); s.save(OUT+'05-detalhes.jpg',quality=95)
    s=Image.new('RGB',(W_,H_),NAVY); d=ImageDraw.Draw(s); L=logo(300); s.paste(L,(60,56),L)
    d.text((72,250),'Condições',font=sans(40,'sb'),fill=GOLD); d.text((68,305),'R$ '+C['preco'],font=wide(112,850),fill=WHITE)
    d.line((72,480,1008,480),fill=GOLD,width=3)
    d.text((72,530),'Pagamento no cartão ou',font=wide(50,800),fill=WHITE); d.text((72,600),'cheque, sob consulta.',font=wide(50,800),fill=WHITE)
    d.text((72,720),'Chame no WhatsApp e receba o vídeo',font=sans(36,'m'),fill=MUTE); d.text((72,768),'dele funcionando.',font=sans(36,'m'),fill=MUTE)
    d.line((72,1100,1008,1100),fill=GOLD,width=3); info_cols(d,1120,COLS); footer(s,d,1238); s.save(OUT+'06-condicoes.jpg',quality=95)
    s=base(280,820); d=ImageDraw.Draw(s)
    d.text((68,880),'Seu verão',font=wide(96,850),fill=WHITE); d.text((68,985),'começa aqui.',font=wide(96,850),fill=TAG)
    d.line((72,1120,1008,1120),fill=GOLD,width=3); d.text((72,1145),'Comente EU QUERO ou chame no WhatsApp',font=sans(30,'sb'),fill=WHITE)
    L=logo(250); s.paste(L,(72,1215),L); t2='(44) 99884-6314'; d.text((1008-d.textlength(t2,font=wide(34,800)),1245),t2,font=wide(34,800),fill=WHITE)
    s.save(OUT+'07-cta.jpg',quality=95)
    q=P.crop((0,330,1080,1410)); fade_to_navy(q,560,740); d=ImageDraw.Draw(q)
    d.text((72,690),MAR,font=sans(36,'sb'),fill=GOLD); d.text((68,738),MOD,font=wide(88,850),fill=WHITE)
    d.line((72,862,1008,862),fill=GOLD,width=3); info_cols(d,878,COLS); footer(q,d,982)
    t=tag(C['preco'],TAGSUB,w=360,angle=6); q.paste(t,(540,450),t); q.save(OUT+'quadrado-facebook.jpg',quality=95)
    st=P.copy(); fade_to_navy(st,1150,1400); d=ImageDraw.Draw(st)
    top=Image.new('RGBA',(1080,420),(0,0,0,0)); td=ImageDraw.Draw(top)
    for y in range(420): td.line((0,y,1080,y),fill=NAVY+(int(200*(1-y/420)),))
    st.paste(top,(0,0),top); L=logo(300); st.paste(L,(390,110),L)
    d.text((72,1420),MAR,font=sans(44,'sb'),fill=GOLD); d.text((68,1485),MOD,font=wide(C.get('model_size',104),850),fill=WHITE)
    d.line((72,1640,1008,1640),fill=GOLD,width=3); info_cols(d,1665,COLS)
    t=tag(C['preco'],TAGSUB,w=400,angle=6); st.paste(t,(480,1150),t)
    d.rounded_rectangle((72,1800,1008,1880),radius=40,outline=WHITE,width=3)
    tx='[ cole aqui o link do WhatsApp ]'; d.text((540-d.textlength(tx,font=sans(30,'m'))/2,1822),tx,font=sans(30,'m'),fill=MUTE); st.save(OUT+'story-1-oferta.jpg',quality=95)
    st=kit.studio(1080,1920,cy=1000); d=ImageDraw.Draw(st); L=logo(300); st.paste(L,(390,110),L)
    d.text((540,330),'QUIZ',font=sans(44,'sb'),fill=GOLD,anchor='ma'); d.text((540,400),C['quiz_l1'],font=wide(80,850),fill=WHITE,anchor='ma'); d.text((540,500),C['quiz_l2'],font=wide(80,850),fill=WHITE,anchor='ma')
    kit.place_jet(st,sj(900),XL(90),700); d=ImageDraw.Draw(st)
    d.rounded_rectangle((140,1560,940,1700),radius=30,outline=TAG,width=3)
    d.text((540,1630),f"[ coloque aqui a figurinha QUIZ: {C['quiz_opts']} ]",font=sans(28,'m'),fill=MUTE,anchor='mm'); st.save(OUT+'story-2-quiz.jpg',quality=95)
    print('imagens ok')
if ONLY in('all','reels'):
    BG=kit.studio(W,H,cy=1050); DARK=Image.new('RGB',(W,H),NAVY2)
    PP=P.resize((1620,2880),Image.LANCZOS)
    def view(cx,cy,z):
        w=W/z; h=H/z; cx=min(max(cx,w/2),W-w/2); cy=min(max(cy,h/2),H-h/2)
        return PP.crop(tuple(int(v*1.5) for v in (cx-w/2,cy-h/2,cx+w/2,cy+h/2))).resize((W,H),Image.BILINEAR)
    def ti(t,font,fill):
        d=ImageDraw.Draw(Image.new('L',(1,1))); b=d.textbbox((0,0),t,font=font)
        im=Image.new('RGBA',(b[2]-b[0]+20,b[3]-b[1]+20),(0,0,0,0)); ImageDraw.Draw(im).text((10-b[0],10-b[1]),t,font=font,fill=fill); return im
    def pc(bg,im,cx,cy,sc=1.0,al=1.0):
        if sc!=1: im=im.resize((max(1,int(im.width*sc)),max(1,int(im.height*sc))),Image.LANCZOS)
        if al<1: im=im.copy(); im.putalpha(im.split()[3].point(lambda v:int(v*al)))
        bg.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
    LG=logo(320); TAGI=tag(C['preco'],TAGSUB,w=480,angle=0)
    def jetframe(t,d,jy=760,w=900):
        fr=BG.copy(); z=1+0.05*t/max(d,1); jw=int(w*z); kit.place_jet(fr,sj(jw),XL((W-jw)/2),jy); pc(fr,LG,W/2,150); return fr
    def endcard(t,d):
        e=eo(seg(t,0,0.4)); fr=Image.new('RGB',(W,H),NAVY); dr=ImageDraw.Draw(fr)
        L=logo(700); fr.paste(L,(int(W/2-350),int(520-40*(1-e))),L)
        dr.text((W/2,860),'Seu verão começa aqui.',font=wide(58,850),fill=WHITE,anchor='mm'); dr.line((140,950,940,950),fill=GOLD,width=3)
        dr.text((W/2,1030),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((W/2,1110),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
        dr.text((W/2,1220),'ou comente EU QUERO',font=sans(40,'sb'),fill=GOLD,anchor='mm'); return fr
    PANEL_A=np.zeros((H,1))
    for y in range(H): PANEL_A[y]=0 if y<1180 else min(1,((y-1180)/240)**1.3)
    PM=Image.fromarray((np.repeat(PANEL_A,W,1)*255).astype('uint8')); PN=Image.new('RGB',(W,H),NAVY)
    TOPG=Image.new('RGBA',(W,360),(0,0,0,0)); td=ImageDraw.Draw(TOPG)
    for y in range(360): td.line((0,y,W,y),fill=NAVY+(int(190*(1-y/360)),))
    def chrome(fr):
        fr.paste(PN,(0,0),PM); fr.paste(TOPG,(0,0),TOPG); fr.paste(LG,(int(W/2-LG.width/2),90),LG)
    def photoscene(v0,v1,l1,l2,small=False):
        def f(t,d):
            q=eio(seg(t,0,d)); fr=view(*[v0[j]+(v1[j]-v0[j])*q for j in range(3)]); chrome(fr)
            dr=ImageDraw.Draw(fr); s=eo(seg(t,0,0.35)); dx=int(-60*(1-s))
            if small: dr.text((72+dx,1350),l1,font=sans(46,'sb'),fill=GOLD); dr.text((68+dx,1405),l2,font=wide(96,850),fill=WHITE)
            else: dr.text((68+dx,1340),l1,font=wide(72,850),fill=WHITE); dr.text((68+dx,1435),l2,font=wide(72,850),fill=TAG)
            dr.line((72,1580,1008,1580),fill=GOLD,width=3); info_cols(dr,1600,COLS); return fr
        return f
    def pricescene(t,d):
        fr=photoscene((540,960,1.0),(540,940,1.05),MAR,MOD,True)(t,d); ang=10*math.exp(-4*t)*math.cos(9*t)
        im=TAGI.rotate(6+ang,resample=Image.BICUBIC,expand=True); pc(fr,im,760,1150-260*(1-eo(seg(t,0,0.5)))); return fr
    def card(n,title,sub,v0,v1):
        def f(t,d):
            q=eio(seg(t,0,d)); fr=view(*[v0[j]+(v1[j]-v0[j])*q for j in range(3)]); chrome(fr); dr=ImageDraw.Draw(fr)
            s=eob(seg(t,0,0.35)); pc(fr,ti(n,wide(150,900),TAG),150,1430,sc=0.6+0.4*s)
            dr.text((280,1350),title,font=wide(60,850),fill=WHITE); dr.text((282,1440),sub,font=sans(40,'sb'),fill=MUTE); return fr
        return f
    V=[tuple(v) for v in C['views']]  # 6 enquadramentos (cx,cy,z) usados nas cenas
    R=C['reel']
    # REEL 1 estúdio
    H1=ti(R['hook1'],wide(116,900),TAG); H2=ti(R['hook2'],wide(104,900),WHITE)
    def s1(t,d):
        fr=DARK.copy(); pc(fr,H1,W/2,760,sc=1+1.2*(1-eo(seg(t,0,0.3))),al=min(1,seg(t,0,0.2)*2))
        if t>0.9: pc(fr,H2,W/2,920,sc=1+1.2*(1-eo(seg(t,0.9,1.2))),al=min(1,seg(t,0.9,1.1)*2))
        return fr
    TM=ti(f"{MAR} {MOD} · {C['ano']}",wide(50,850),TAG)
    def s2(t,d):
        fr=BG.copy(); r_=eo(seg(t,0,0.9)); jw=int(900*(0.85+0.15*r_)); j=sj(jw)
        if r_<1: j=j.copy(); j.putalpha(j.split()[3].point(lambda v:int(v*min(1,r_*1.4))))
        kit.place_jet(fr,j,XL((W-jw)/2),760+260*(1-r_)); pc(fr,LG,W/2,150); pc(fr,TM,W/2,330,al=seg(t,0.3,0.7)); return fr
    HPN=int(C['hp'])
    def s3(t,d):
        fr=jetframe(t,d); c=int(HPN*eo(seg(t,0.1,1.4))); pc(fr,ti(f'{c} hp',wide(170,900),TAG),W/2,480)
        pc(fr,ti(R['motor_tag'],sans(48,'sb'),WHITE),W/2,620,al=seg(t,0.3,0.6)); return fr
    def s4(t,d):
        fr=jetframe(t+3,d+3)
        for k,it in enumerate(R['pills']):
            s=seg(t,0.2+k*0.6,0.5+k*0.6)
            if s>0:
                im=Image.new('RGBA',(860,110),(0,0,0,0)); dd=ImageDraw.Draw(im); dd.rounded_rectangle((0,0,859,109),radius=55,fill=(16,30,50),outline=TAG,width=3)
                dd.text((430,55),it,font=wide(38,850),fill=WHITE,anchor='mm'); pc(fr,im,W/2+80*(1-eo(s)),380+k*135,al=s)
        return fr
    def s5(t,d):
        fr=BG.copy(); kit.place_jet(fr,sj(900),XL(90),520); pc(fr,LG,W/2,150)
        ang=10*math.exp(-4*t)*math.cos(9*t); im=TAGI.rotate(6+ang,resample=Image.BICUBIC,expand=True); pc(fr,im,W/2+40,1330-260*(1-eo(seg(t,0,0.5)))); return fr
    sc1=[dict(spk=R['r1'][0],cap=None,draw=s1,flash=False,min=2.6)]
    for (spk,cap),fn,yc in zip(R['r1'][1:5],[s2,s3,s4,s5],[1640,1640,1640,1060]): sc1.append(dict(spk=spk,cap=cap,draw=fn,ycap=yc))
    sc1.append(dict(spk='Comenta eu quero, ou chama a Cântri no zap!',cap='Comente EU QUERO ou chama a Country no zap!',draw=endcard,ycap=1450,min=3.0))
    print('R1',build(sc1,OUT+'reel-1-potencia.mp4'))
    # REEL 2 foto
    sc2=[]
    for k,(spk,cap,l1,l2) in enumerate(R['r2']):
        sc2.append(dict(spk=spk,cap=cap,draw=photoscene(V[k%len(V)],V[(k+1)%len(V)],l1,l2),flash=k>0))
    sc2.append(dict(spk=R['r2_price'][0],cap=R['r2_price'][1],draw=pricescene))
    sc2.append(dict(spk='Cântri Negócios.',cap=None,draw=endcard,min=2.6))
    print('R2',build(sc2,OUT+'reel-2-equipado.mp4',ycap=1010))
    # REEL 3 dor
    HK=[ti(R['r3_hook'][0],wide(92,900),WHITE),ti(R['r3_hook'][1],wide(92,900),TAG),ti(R['r3_hook'][2],sans(56,'sb'),WHITE)]
    def hook(t,d):
        fr=view(540,960-40*t,1.1+0.05*t); ov=Image.new('RGBA',(W,H),NAVY2+(170,)); fr.paste(ov,(0,0),ov)
        pc(fr,HK[0],W/2,760,sc=1+0.8*(1-eo(seg(t,0,0.25))))
        if t>0.35: pc(fr,HK[1],W/2,880,sc=1+0.8*(1-eo(seg(t,0.35,0.6))))
        if t>0.8: pc(fr,HK[2],W/2,1000,al=seg(t,0.8,1.0))
        pc(fr,LG,W/2,150); return fr
    sc3=[dict(spk=R['r3_hook_spk'],cap=None,draw=hook,flash=False)]
    for k,(spk,cap,n,t1,t2) in enumerate(R['r3']):
        sc3.append(dict(spk=spk,cap=cap,draw=card(n,t1,t2,V[(k+1)%len(V)],V[(k+2)%len(V)]),ycap=1000))
    sc3.append(dict(spk=R['r3_price'][0],cap=R['r3_price'][1],draw=pricescene,ycap=1010))
    sc3.append(dict(spk='Chama no zap e vem ver de perto!',cap='Chama no zap e vem ver de perto!',draw=endcard,ycap=1450,min=2.8))
    print('R3',build(sc3,OUT+'reel-3-dor.mp4',ycap=1010))
