import sys,subprocess; sys.path.insert(0,'.')
from country import *
import country as C
W,H,FPS=1080,1920,30; DUR=13.0; N=int(DUR*FPS)
def eo(t): t=max(0,min(1,t)); return 1-(1-t)**3
def eio(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
P=C.photo_portrait().resize((1620,2880),Image.LANCZOS); S=1.5
def view(cx,cy,z):
    w=W/z; h=H/z; cx=min(max(cx,w/2),W-w/2); cy=min(max(cy,h/2),H-h/2)
    return P.crop(tuple(int(v*S) for v in (cx-w/2,cy-h/2,cx+w/2,cy+h/2))).resize((W,H),Image.BILINEAR)
shots=[(0,3.0,(540,900,1.25),(540,960,1.05)),(3.0,5.8,(620,600,1.7),(580,640,1.5)),(5.8,8.6,(430,1050,1.45),(480,1000,1.3)),(8.6,11.2,(540,860,1.15),(540,960,1.0))]
PANEL=Image.new('RGBA',(W,H),(0,0,0,0)); a=np.zeros((H,1))
for y in range(H): a[y]=0 if y<1180 else min(1,((y-1180)/240)**1.3)
PANEL=Image.new('RGB',(W,H),NAVY); PM=Image.fromarray((np.repeat(a,W,1)*255).astype('uint8'))
TOPG=Image.new('RGBA',(W,360),(0,0,0,0)); td=ImageDraw.Draw(TOPG)
for y in range(360): td.line((0,y,W,y),fill=NAVY+(int(190*(1-y/360)),))
LG=C.logo(320); TAGI=C.tag('105.000','ou 18x no cartão',w=430,angle=0)
caps=[('Procurando jet ski','pro verão?'),('Sea-Doo','GTI 2024'),('Só 89 horas','de uso'),('Sea-Doo','GTI 2024')]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
 '-f','lavfi','-t',str(DUR),'-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-c:a','aac','-movflags','+faststart',OUT+'reel-02-loja.mp4'],stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    if t<11.2:
        for k,(a0,b0,v0,v1) in enumerate(shots):
            if a0<=t<b0:
                q=eio(seg(t,a0,b0)); fr=view(*[v0[j]+(v1[j]-v0[j])*q for j in range(3)])
                if t-a0<0.1 and a0>0: fr=Image.blend(fr,Image.new('RGB',(W,H),WHITE),0.45*(1-(t-a0)/0.1))
                break
        fr.paste(PANEL,(0,0),PM); fr.paste(TOPG,(0,0),TOPG); fr.paste(LG,(int(W/2-LG.width/2),90),LG)
        d=ImageDraw.Draw(fr); s=eo(seg(t,a0,a0+0.35)); dx=int(-60*(1-s))
        l1,l2=caps[k]
        if k==1 or k==3:
            d.text((72+dx,1350),l1,font=sans(46,'sb'),fill=GOLD); d.text((68+dx,1405),l2,font=wide(104,850),fill=WHITE)
        else:
            d.text((68+dx,1340),l1,font=wide(78,850),fill=WHITE); d.text((68+dx,1440),l2,font=wide(78,850),fill=TAG)
        d.line((72,1580,72+int(936*eo(seg(t,0.2,1.0))),1580),fill=GOLD,width=3)
        info_cols(d,1600,[('Ano','2024'),('Horas de uso','89'),('Lugares','3')])
        if k==3:
            ang=10*math.exp(-4*(t-a0))*math.cos(9*(t-a0))
            ti=TAGI.rotate(6+ang,resample=Image.BICUBIC,expand=True)
            y=int(930-300*(1-eo(seg(t,a0,a0+0.5)))); fr.paste(ti,(430,y),ti)
    else:
        e=eo(seg(t,11.2,11.6)); fr=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(fr)
        L=C.logo(700); fr.paste(L,(int(W/2-350),int(560-40*(1-e))),L)
        d.text((W/2,900),'Seu verão começa aqui.',font=wide(58,850),fill=WHITE,anchor='mm')
        d.line((140,990,940,990),fill=GOLD,width=3)
        d.text((W/2,1070),'Chame no WhatsApp',font=sans(44,'m'),fill=MUTE,anchor='mm')
        d.text((W/2,1150),'(44) 99884-6314',font=wide(70,850),fill=WHITE,anchor='mm')
        d.text((W/2,1260),'ou comente EU QUERO',font=sans(40,'sb'),fill=GOLD,anchor='mm')
    proc.stdin.write(fr.tobytes())
proc.stdin.close(); proc.wait(); print('done')
