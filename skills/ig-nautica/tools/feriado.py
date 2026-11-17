import sys; sys.path.insert(0,'.')
from best import *
OUT='/home/user/instagram-agent-skill/midia/feriado-duas-lanchas/'
NV2=(32,54,84)
def ph(n,w,h,cy=0.5,zoom=1.0): return hero(n,0.5,cy,zoom,w,h)
def check(d,x,y,t,f):
    d.ellipse((x,y+4,x+34,y+38),fill=GD); d.line((x+8,y+21,x+15,y+29,x+27,y+13),fill=NV3,width=4); d.text((x+48,y),t,font=f,fill=IV)
def card(s,x,y,w,h,name,photos,items,tag,fb=0.40,fs=0.20,gap=52):
    d=ImageDraw.Draw(s); d.rounded_rectangle((x,y,x+w,y+h),radius=28,fill=NV2)
    big=ph(photos[0][0],w-28,int(h*fb),photos[0][1]); tile(s,big,x+14,y+14,r=20)
    sw=(w-28-12)//2; sy=y+14+big.height+12
    for i,(n,cy) in enumerate(photos[1:]): tile(s,ph(n,sw,int(h*fs),cy),x+14+i*(sw+12),sy,r=16)
    d=ImageDraw.Draw(s); ty=sy+int(h*fs)+20
    d.text((x+28,ty),name,font=serif(64,600),fill=IV,features=['lnum'])
    d.rounded_rectangle((x+w-28-d.textlength(tag,font=sans(20,'b'))-32,ty+16,x+w-28,ty+56),radius=20,fill=GD); d.text((x+w-44,ty+36),tag,font=sans(20,'b'),fill=NV3,anchor='rm')
    for k,t in enumerate(items): check(d,x+28,ty+86+k*gap,t,sans(30,'sb'))
def make(W,H,fn,story=False):
    yy=np.linspace(0,1,H)[:,None]; g=np.array([30,52,80])*(1-yy)+np.array(NV3)*yy
    s=Image.fromarray(np.repeat(g[:,None,:],W,1).astype('uint8')); d=ImageDraw.Draw(s)
    y0=40 if not story else 90
    c=LC.resize((86,86),Image.LANCZOS); s.paste(c,(W//2-43,y0),c); sp(d,W//2,y0+100,'COUNTRY NEGÓCIOS',sans(18,'sb'),IV,s=8)
    d.rounded_rectangle((W//2-230,y0+140,W//2+230,y0+192),radius=26,fill=GD); sp(d,W//2,y0+153,'FERIADÃO · SEXTA 20/11',sans(24,'b'),NV3,s=4)
    d.text((W//2,y0+210),'Alugue sua lancha',font=serif(84 if not story else 92,600),fill=IV,anchor='ma')
    d.text((W//2,y0+300),'em Porto Rico.',font=serif(84 if not story else 92,500,True),fill=GD,anchor='ma')
    cy=y0+(410 if not story else 430); ch=H-cy-(150 if not story else 260); cw=(W-3*36)//2
    card(s,36,cy,cw,ch,'NHD 280',[('6c842673',0.5),('a37e75d6',0.5),('ca86e549',0.55)],['Rabeta Bravo','Quarto na cabine','Banheiro','Churrasqueira'],'COM QUARTO',*( (0.40,0.20,52) if story else (0.33,0.17,46) ))
    card(s,72+cw,cy,cw,ch,'NX 250',[('1d5d97b3',0.45),('3603af94',0.3),('9667fb83',0.45)],['Rabeta Bravo','Banheiro','Até 10 pessoas','Som de festa'],'PROA ABERTA',*( (0.40,0.20,52) if story else (0.33,0.17,46) ))
    d=ImageDraw.Draw(s); by=H-(120 if not story else 220)
    f=sans(28,'b'); t='RESERVE JÁ  ·  (44) 99884-6314'; w=sum(d.textlength(ch_,font=f) for ch_ in t)+4*(len(t)-1)
    d.rounded_rectangle((W//2-w/2-50,by,W//2+w/2+50,by+80),radius=40,fill=GD); sp(d,W//2,by+24,t,f,NV3,s=4)
    if story: d.text((W//2,by+110),'As datas do feriado acabam rápido.',font=serif(40,500,True),fill=(222,214,198),anchor='ma')
    s.save(OUT+fn,quality=97); return s
a=make(1080,1350,'post-feriado-duas-lanchas.jpg'); b=make(1080,1920,'status-whatsapp.jpg',story=True)
cv=Image.new('RGB',(540+380+10,675),'white'); cv.paste(a.resize((540,675)),(0,0)); cv.paste(b.resize((380,675)),(550,0)); cv.save('/tmp/claude-0/fer_prev.jpg'); print('ok')
