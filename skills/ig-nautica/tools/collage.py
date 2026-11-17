import sys; sys.path.insert(0,'.')
from nhd import *
NV=(22,39,60); NV2=(34,56,86); NV3=(9,17,29); GD=(196,152,90); IV=(247,246,242); MU=(176,186,202)
LC=Image.open('/tmp/claude-0/logo_circle.png')
def lc(sz): return LC.resize((sz,sz),Image.LANCZOS)
def cond(sz,w=900): return wide(sz,w,62)
W_,H_=1080,1350; M=56
def ph(n,w,h,cx=0.5,cy=0.5,zoom=1.0):
    im=fit(P(n),w,h,cx=cx,cy=cy,zoom=zoom); return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.1)).enhance(1.08)
def brand(s,d,x=M,y=40,col=IV,sub=GD):
    c=lc(90); s.paste(c,(x,y),c); d.text((x+108,y+20),'COUNTRY',font=wide(28,900),fill=col); d.text((x+110,y+56),'N E G Ó C I O S',font=sans(15,'sb'),fill=sub)
def pill(d,x,y,t,bg=GD,fg=NV,f=None,anchor='l'):
    f=f or sans(26,'b'); w=d.textlength(t,font=f)
    if anchor=='c': x=x-(w+44)/2
    d.rounded_rectangle((x,y,x+w+44,y+54),radius=27,fill=bg); d.text((x+22,y+27),t,font=f,fill=fg,anchor='lm'); return w+44
def foot(s,d,y=H_-92):
    d.rectangle((0,y-14,W_,H_),fill=NV3); d.text((M,y+8),'RESERVAS',font=sans(22,'b'),fill=GD); d.text((M+140,y),'(44) 99884-6314',font=cond(52),fill=IV)
    d.text((W_-M,y+10),'Porto Rico · PR',font=sans(24,'sb'),fill=MU,anchor='ra')
def run(cfg,out):
    os.makedirs(out,exist_ok=True); A=cfg['ph']; name=cfg['nome']; tags=cfg['tags']
    # A · MOSAICO
    s=Image.new('RGB',(W_,H_),NV); d=ImageDraw.Draw(s); brand(s,d); pill(d,W_-M-330,58,'ALUGUEL · FIM DE SEMANA',f=sans(22,'b'))
    d.text((M-4,150),name,font=cond(150),fill=IV)
    tile(s,ph(*A['hero']),M,330,r=24)
    w3=(W_-2*M-2*16)//3
    for i,k in enumerate(A['row3']): tile(s,ph(k[0],w3,250,*k[1:]),M+i*(w3+16),330+A['hero'][2]+16,r=20)
    d=ImageDraw.Draw(s); x=M
    for t in tags: x+=pill(d,x,1145,t,bg=NV2,fg=IV,f=sans(24,'b'))+10
    foot(s,d); s.save(out+'post-A-mosaico.jpg',quality=97)
    # B · GRADE com selo central
    s=Image.new('RGB',(W_,H_),NV3); g=8; cw=(W_-g)//2; rh=(H_-110-2*g)//3
    d=ImageDraw.Draw(s)
    for i,k in enumerate(A['grid6']):
        x,y=(i%2)*(cw+g),(i//2)*(rh+g)
        if k[0]=='TXT': d.rectangle((x,y,x+cw,y+rh),fill=GD); d.text((x+cw/2,y+rh/2-50),k[1],font=cond(110),fill=NV,anchor='mm'); d.text((x+cw/2,y+rh/2+50),k[2],font=sans(28,'b'),fill=NV,anchor='mm')
        else: s.paste(ph(k[0],cw,rh,*k[1:]),(x,y)); cx,cy=W_//2,(H_-110)//2
    d.ellipse((cx-200,cy-200,cx+200,cy+200),fill=NV,outline=GD,width=6); c=lc(120); s.paste(c,(cx-60,cy-175),c)
    d.text((cx,cy-30),name,font=cond(96),fill=IV,anchor='ma'); d.text((cx,cy+80),'ALUGUEL',font=sans(26,'b'),fill=GD,anchor='ma'); d.text((cx,cy+115),'FIM DE SEMANA',font=sans(22,'sb'),fill=MU,anchor='ma')
    foot(s,d); s.save(out+'post-B-grade.jpg',quality=97)
    # C · POLAROIDS
    s=Image.new('RGB',(W_,H_),NV); d=ImageDraw.Draw(s)
    yy=np.linspace(0,1,H_)[:,None]; gr=np.array(NV2)*(1-yy)+np.array(NV3)*yy; s=Image.fromarray(np.repeat(gr[:,None,:],W_,1).astype('uint8')); d=ImageDraw.Draw(s)
    brand(s,d); d.text((M-4,150),'SEU FIM DE SEMANA',font=cond(80),fill=IV); d.text((M-4,240),'A BORDO DA '+name,font=cond(80),fill=GD)
    spots=[(80,350,-5),(570,340,4),(90,775,4),(575,765,-4)]
    for (x,y,rot),(k,lb) in zip(spots,A['pola4']):
        im=ph(k[0],390,290,*k[1:]); card=Image.new('RGB',(430,380),IV); card.paste(im,(20,20)); cd=ImageDraw.Draw(card); cd.text((215,342),lb,font=sans(28,'b'),fill=NV,anchor='mm')
        sh=Image.new('RGBA',(500,490),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((30,36,460,416),fill=(0,0,0,120)); sh=sh.filter(ImageFilter.GaussianBlur(14))
        card=card.convert('RGBA'); sh.alpha_composite(card,(30,30)); sh=sh.rotate(rot,resample=Image.BICUBIC,expand=True); s.paste(sh,(x-30,y-30),sh)
    d=ImageDraw.Draw(s); foot(s,d); s.save(out+'post-C-polaroid.jpg',quality=97)
    # D · REVISTA (split)
    s=Image.new('RGB',(W_,H_),IV); d=ImageDraw.Draw(s); lw=600; hh=H_-110
    s.paste(ph(A['tall'][0],lw,hh,*A['tall'][1:]),(0,0))
    ov=Image.new('RGBA',(lw,hh),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for y in range(620): od.line((0,y,lw,y),fill=NV3+(int(245*(1-y/620)**0.8),))
    s.paste(ov,(0,0),ov); d=ImageDraw.Draw(s); brand(s,d)
    d.text((M-4,170),name,font=cond(120),fill=IV); d.text((M,300),'ALUGUEL · FIM DE SEMANA',font=sans(24,'b'),fill=GD)
    rw=W_-lw-16; rh2=(hh-2*16)//3
    for i,k in enumerate(A['col3']): s.paste(ph(k[0],rw,rh2,*k[1:]),(lw+16,i*(rh2+16)))
    d=ImageDraw.Draw(s)
    for i,lb in enumerate(A['col3lab']): pill(d,lw+30,i*(rh2+16)+rh2-70,lb,bg=NV,fg=IV,f=sans(22,'b'))
    foot(s,d); s.save(out+'post-D-revista.jpg',quality=97)
    ims=[Image.open(out+f).resize((324,405)) for f in ['post-A-mosaico.jpg','post-B-grade.jpg','post-C-polaroid.jpg','post-D-revista.jpg']]
    return ims
NHD=dict(nome='NHD 280',tags=['28 pés','280 hp','Cabine com ar','Churrasqueira'],ph=dict(
 hero=('6c842673',W_-2*M,520,0.5,0.5),row3=[('ca86e549',0.55),('a37e75d6',0.5),('819e42ac',0.42)],
 grid6=[('6c842673',0.5),('ca86e549',0.55),('a37e75d6',0.5),('494e31cb',0.45),('14540dc4',0.45),('819e42ac',0.45)],
 pola4=[(('ca86e549',0.55),'Churrasqueira'),(('a37e75d6',0.5),'Cabine com ar'),(('6c842673',0.5),'Espaço'),(('819e42ac',0.42),'Som')],
 tall=('6c842673',0.55),col3=[('ca86e549',0.55),('a37e75d6',0.5),('550c4289',0.5)],col3lab=['Churrasqueira','Cabine com ar','Banheiro']))
NX=dict(nome='NX 250',tags=['25 pés','Até 10 pessoas','Som de festa'],ph=dict(
 hero=('1d5d97b3',W_-2*M,520,0.5,0.45),row3=[('3603af94',0.3),('f6dce81e',0.42),('aafe8b4b',0.4)],
 grid6=[('1d5d97b3',0.45),('3603af94',0.3),('f6dce81e',0.42),('aafe8b4b',0.4),('9667fb83',0.4),('TXT','10','PESSOAS · SOM DE FESTA')],
 pola4=[(('3603af94',0.3),'Proa'),(('9667fb83',0.45),'Som'),(('f6dce81e',0.42),'Cockpit'),(('aafe8b4b',0.4),'Popa')],
 tall=('9667fb83',0.5,1.0),col3=[('3603af94',0.3),('f6dce81e',0.42),('aafe8b4b',0.4)],col3lab=['Proa com sofá em U','Cockpit','Popa com som']))
O='/home/user/instagram-agent-skill/midia/'
a=run(NHD,O+'aluguel-nhd280-country/'); b=run(NX,O+'aluguel-nx250-country/')
c=Image.new('RGB',(334*4,820),'white')
for i,im in enumerate(a): c.paste(im,(i*334,0))
for i,im in enumerate(b): c.paste(im,(i*334,415))
c.save('/tmp/claude-0/col_prev.jpg'); print('ok')
