import sys,json; sys.path.insert(0,'.')
from motor import *
import real
C=json.load(open(sys.argv[1])); OUT=C['sr_out']; os.makedirs(OUT,exist_ok=True)
J=Image.open(C['cut']).convert('RGBA'); J=J.crop(J.getbbox())
if C.get('sr_kill_bottom'): 
    a=np.array(J).astype(float); h=a.shape[0]; c=int(h*C['sr_kill_bottom']); a[...,3]*=np.clip((c-np.arange(h))/6,0,1)[:,None]; J=Image.fromarray(a.astype('uint8'),'RGBA')
WL=C.get('sr_wl',0.80); RIGHT=C.get('jet_right',False); LEFT=C.get('jet_left',False)
def jx(w,cw=1080): return cw-w+10 if RIGHT else (-10 if LEFT else (cw-w)//2)
CREDIT='Cenário: Praia de Santa Rosa, Porto Rico (foto Roberto Dziura Jr./AEN) · montagem ilustrativa'
def credit(im,y=None):
    d=ImageDraw.Draw(im); y=y or im.height-26; d.text((im.width/2,y),CREDIT,font=sans(17,'m'),fill=(235,238,240),anchor='mm',stroke_width=2,stroke_fill=(20,25,30))
def pin(d,x,y,txt):
    w=d.textlength(txt,font=sans(30,'sb')); d.rounded_rectangle((x,y,x+w+80,y+58),radius=29,fill=(255,255,255,235))
    d.ellipse((x+20,y+17,x+44,y+41),fill=(220,60,50)); d.ellipse((x+28,y+25,x+36,y+33),fill=WHITE); d.text((x+56,y+12),txt,font=sans(30,'sb'),fill=NAVY2)
def glass(im,box,alpha=185):
    x0,y0,x1,y1=box; reg=im.crop(box).filter(ImageFilter.GaussianBlur(20)); im.paste(reg,(x0,y0))
    ov=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle(box,radius=34,fill=NAVY2+(alpha,),outline=(255,255,255,50),width=2); im.paste(ov,(0,0),ov)
MOD=C['modelo']; ANO=C['ano']; HRS=C['horas']; HP=C['hp']; PR=C['preco']
# ---- FEED 4:5 ----
bg=real.bg_crop('ilha_carioca_foto_rdzura-1754.jpg',1080,1350,cx_frac=0.5,cy_frac=0.55)
jw=C.get('sr_w',740); Jr=J.resize((jw,int(J.height*jw/J.width)),Image.LANCZOS)
real.place(bg,Jr,jx(jw),int(1350*0.80-Jr.height*WL),wl=WL)
bg=bg.convert('RGBA'); d=ImageDraw.Draw(bg)
top=Image.new('RGBA',(1080,380),(0,0,0,0)); td=ImageDraw.Draw(top)
for yy in range(380): td.line((0,yy,1080,yy),fill=NAVY2+(int(170*(1-yy/380)),))
bg.alpha_composite(top); d=ImageDraw.Draw(bg)
L=logo(250); bg.alpha_composite(L,(60,50))
d.text((64,150),C['marca'],font=sans(38,'sb'),fill=TAG); d.text((58,195),MOD,font=wide(104,900),fill=WHITE)
d.text((64,330),f'{ANO}  ·  {HRS} horas  ·  {HP} hp',font=sans(36,'sb'),fill=WHITE)
pin(d,620,60,'Prainha de Santa Rosa')
bg=bg.convert('RGB'); glass(bg,(50,1110,1030,1290)); d=ImageDraw.Draw(bg)
d.text((90,1132),'R$ '+PR,font=wide(70,900),fill=WHITE); d.text((92,1228),'Chame no WhatsApp  (44) 99884-6314',font=sans(30,'sb'),fill=TAG)
credit(bg,1322); bg.save(OUT+'feed-santa-rosa.jpg',quality=96)
# ---- STORY 9:16 ----
st=real.bg_crop('ilha_carioca_foto_rdzura-1754.jpg',1080,1920,cx_frac=0.52,cy_frac=0.5)
jw2=C.get('sr_w_story',820); J2=J.resize((jw2,int(J.height*jw2/J.width)),Image.LANCZOS)
real.place(st,J2,jx(jw2),int(1920*0.72-J2.height*WL),wl=WL,seed=3)
st=st.convert('RGBA'); top=Image.new('RGBA',(1080,520),(0,0,0,0)); td=ImageDraw.Draw(top)
for yy in range(520): td.line((0,yy,1080,yy),fill=NAVY2+(int(180*(1-yy/520)),))
st.alpha_composite(top); d=ImageDraw.Draw(st); L=logo(300); st.alpha_composite(L,(390,110))
pin(d,540-int(d.textlength('Prainha de Santa Rosa',font=sans(30,'sb'))/2)-40,250,'Prainha de Santa Rosa')
d.text((540,360),MOD,font=wide(110,900),fill=WHITE,anchor='ma')
st=st.convert('RGB'); glass(st,(60,1500,1020,1760)); d=ImageDraw.Draw(st)
d.text((540,1525),f'{ANO} · {HRS} horas · {HP} hp',font=sans(38,'sb'),fill=TAG,anchor='ma')
d.text((540,1585),'R$ '+PR,font=wide(86,900),fill=WHITE,anchor='ma')
d.rounded_rectangle((140,1790,940,1870),radius=40,outline=WHITE,width=3); d.text((540,1830),'[ cole aqui o link do WhatsApp ]',font=sans(28,'m'),fill=(225,230,235),anchor='mm')
credit(st,1895); st.save(OUT+'story-santa-rosa.jpg',quality=96)
print('imagens ok')
# ---- REEL ----
if len(sys.argv)>2 and sys.argv[2]=='reel':
    AER=Image.open(real.SR+'praia_santa_rosa_foto_rdzura-0085.jpg').convert('RGB')
    def aerial(t,d_):
        z=1.0+0.12*t/d_; ch=int(2000/z); cw=int(ch*9/16); x0=int(1500-cw/2+120*t/d_); y0=int((2000-ch)/2)
        fr=AER.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        fr=fr.convert('RGBA'); top=Image.new('RGBA',(W,560),(0,0,0,0)); td=ImageDraw.Draw(top)
        for yy in range(560): td.line((0,yy,W,yy),fill=NAVY2+(int(190*(1-yy/560)),))
        fr.alpha_composite(top); dd=ImageDraw.Draw(fr); L=logo(300); fr.alpha_composite(L,(390,100))
        a=eo(seg(t,0.2,0.7)); 
        if a>0: dd.text((540,300),'PRAINHA DE',font=wide(70,900),fill=(255,255,255,int(255*a)),anchor='ma'); dd.text((540,390),'SANTA ROSA',font=wide(96,900),fill=TAG+(int(255*a),),anchor='ma')
        fr=fr.convert('RGB'); credit(fr,1895); return fr
    BGV=real.bg_crop('ilha_carioca_foto_rdzura-1754.jpg',1240,2204,cx_frac=0.52,cy_frac=0.5)
    jwv=C.get('sr_w_story',820); JV=J.resize((jwv,int(J.height*jwv/J.width)),Image.LANCZOS)
    def comp(t,zoom0=1.0,zoom1=1.08):
        z=zoom0+(zoom1-zoom0)*min(1,t/8); cw=int(1240/z*0.871); ch=int(cw*16/9); x0=(1240-cw)//2; y0=(2204-ch)//2
        b=BGV.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
        y=int(1920*0.72-JV.height*WL+7*math.sin(t*2.1)); x=jx(jwv)+int(4*math.sin(t*1.3))
        real.place(b,JV,x,y,wl=WL,t=t,seed=5); return b
    def sc_text(l1,l2):
        def f(t,d_):
            fr=comp(t+s_off[0]).convert('RGBA'); top=Image.new('RGBA',(W,560),(0,0,0,0)); td=ImageDraw.Draw(top)
            for yy in range(560): td.line((0,yy,W,yy),fill=NAVY2+(int(170*(1-yy/560)),))
            fr.alpha_composite(top); dd=ImageDraw.Draw(fr); L=logo(300); fr.alpha_composite(L,(390,100))
            a=eo(seg(t,0,0.35))
            dd.text((540,290),l1,font=wide(84,900),fill=(255,255,255,int(255*a)),anchor='ma',stroke_width=4,stroke_fill=NAVY2)
            dd.text((540,400),l2,font=wide(64,900),fill=TAG+(int(255*a),),anchor='ma',stroke_width=4,stroke_fill=NAVY2)
            fr=fr.convert('RGB'); credit(fr,1895); return fr
        return f
    s_off=[0]
    def price(t,d_):
        fr=comp(t+9); glass(fr,(70,300,1010,600)); dd=ImageDraw.Draw(fr); a=eo(seg(t,0.1,0.5))
        if a>0: dd.text((540,340),'R$ '+PR,font=wide(96,900),fill=WHITE,anchor='ma'); dd.text((540,480),'(44) 99884-6314',font=wide(54,850),fill=TAG,anchor='ma')
        L=logo(300); fr.paste(L,(390,100),L); credit(fr,1895); return fr
    def endcard(t,d_):
        e=eo(seg(t,0,0.4)); fr=Image.new('RGB',(W,H),NAVY); dr=ImageDraw.Draw(fr)
        L=logo(700); fr.paste(L,(int(W/2-350),int(520-40*(1-e))),L)
        dr.text((W/2,860),'Seu verão começa aqui.',font=wide(58,850),fill=WHITE,anchor='mm'); dr.line((140,950,940,950),fill=GOLD,width=3)
        dr.text((W/2,1030),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm'); dr.text((W/2,1110),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
        dr.text((W/2,1220),'ou comente EU QUERO',font=sans(40,'sb'),fill=GOLD,anchor='mm'); return fr
    R=C['sr_reel']
    sc=[dict(spk=R[0],cap=None,draw=aerial,flash=False,min=3.0),
        dict(spk=R[1][0],cap=R[1][1],draw=sc_text(MOD,f'{ANO} · {HRS} horas'),flash=True,ycap=1560),
        dict(spk=R[2][0],cap=R[2][1],draw=sc_text(f'{HP} CAVALOS',R[2][2]),flash=False,ycap=1560),
        dict(spk=R[3][0],cap=R[3][1],draw=price,flash=False,ycap=1560),
        dict(spk='Cântri Negócios.',cap=None,draw=endcard,min=2.6)]
    print('reel',build(sc,OUT+'reel-santa-rosa.mp4'))
