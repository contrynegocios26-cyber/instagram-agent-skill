import sys,subprocess; sys.path.insert(0,'.')
from kit import *
W,H,FPS=1080,1920,30; DUR=15.0; N=int(DUR*FPS)
def eo(t): t=max(0,min(1,t)); return 1-(1-t)**3
def eob(t):  # ease out back
    t=max(0,min(1,t)); c1=1.70158; c3=c1+1; return 1+c3*(t-1)**3+c1*(t-1)**2
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
BG=studio(W,H,cy=1050)
DARK=Image.new('RGB',(W,H),DEEP)
J=jet(960)
ff=f('black',300)
def textimg(t,font,fill):
    d=ImageDraw.Draw(Image.new('L',(1,1))); b=d.textbbox((0,0),t,font=font)
    im=Image.new('RGBA',(b[2]-b[0]+20,b[3]-b[1]+20),(0,0,0,0)); ImageDraw.Draw(im).text((10-b[0],10-b[1]),t,font=font,fill=fill); return im
def paste_c(bg,im,cx,cy,scale=1.0,alpha=1.0):
    if scale!=1.0: im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.LANCZOS)
    if alpha<1: a=im.split()[3].point(lambda v:int(v*alpha)); im=im.copy(); im.putalpha(a)
    bg.paste(im,(int(cx-im.width/2),int(cy-im.height/2)),im)
T_ELE=textimg('ELE TEM',f('black',110),WHITE)
T_89=textimg('89 HORAS',f('black',190),GOLD2)
T_ZERO=textimg('e parece zero.',f('xb',96),WHITE)
T_MODEL=textimg('SEA-DOO GTI 2024',f('b',54),GOLD2)
T_PRICE=textimg('R$ 105 mil',f('black',150),WHITE)
P18=Image.new('RGBA',(760,120),(0,0,0,0)); pd=ImageDraw.Draw(P18); pill(pd,380,0,'em até 18x no cartão',f('xb',54),GOLD,DEEP,h=116)
T_CTA1=textimg('Comente EU QUERO',f('black',92),WHITE)
T_CTA2=textimg('e a gente te chama no direct',f('m',48),MUTE)
T_BR=textimg('COUNTRY NEGÓCIOS',f('b',46),GOLD2)
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
 '-f','lavfi','-t',str(DUR),'-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-c:a','aac','-movflags','+faststart',OUT+'reel-01-89-horas.mp4'],stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    if t<3.0:
        fr=DARK.copy()
        # gold streak
        if t<2.9:
            a=seg(t,0.0,0.5); paste_c(fr,T_ELE,W/2,700,scale=1+0.6*(1-eob(seg(t,0,0.35))),alpha=a)
            s89=seg(t,0.5,0.85); 
            if s89>0: paste_c(fr,T_89,W/2,920,scale=1+1.5*(1-eo(s89)),alpha=min(1,s89*2))
            sz=seg(t,1.5,1.9)
            if sz>0: paste_c(fr,T_ZERO,W/2,1150+40*(1-eo(sz)),alpha=sz)
            # flash on slam
            fl=seg(t,0.82,1.0)
            if 0<fl<1: fr=Image.blend(fr,Image.new('RGB',(W,H),GOLD2),0.35*(1-fl))
        # wipe to studio
        wp=seg(t,2.6,3.0)
        if wp>0:
            bg=BG.copy(); x=int(W*eo(wp)); fr.paste(bg.crop((0,0,x,H)),(0,0))
    else:
        fr=BG.copy()
        # jet rise + slow zoom
        rise=eo(seg(t,3.0,4.0)); z=1+0.06*seg(t,3,15)
        jw=int(960*z*(0.85+0.15*rise)); j=J.resize((jw,int(J.height*jw/J.width)),Image.LANCZOS)
        jy=780+300*(1-rise)-(250*eo(seg(t,8.3,9.0)))-(0)
        if t>=11.6: jy-=0
        a_j=min(1,seg(t,3.0,3.6)*1.5)
        if a_j<1: al=j.split()[3].point(lambda v:int(v*a_j)); j=j.copy(); j.putalpha(al)
        place_jet(fr,j,(W-jw)/2,jy,refl=a_j>0.9,shadow=a_j>0.5)
        # light sweep across jet
        sw=seg(t,4.0,4.9)
        if 0<sw<1:
            ov=Image.new('L',(W,H),0); od=ImageDraw.Draw(ov); x=-400+1900*sw
            od.polygon([(x,0),(x+160,0),(x-340,H),(x-500,H)],fill=90); ov=ov.filter(ImageFilter.GaussianBlur(30))
            mask=ImageChops.multiply(ov, Image.new('L',(W,H),0) if False else ov)
            fr.paste(WHITE,(0,0),ov)
        # model label
        ml=seg(t,3.6,4.2)
        if ml>0 and t<11.6: paste_c(fr,T_MODEL,W/2,360-30*(1-eo(ml)),alpha=ml)
        # stats sequence 5-8.3
        if 4.8<=t<8.4:
            d=ImageDraw.Draw(fr)
            cnt=int(89*eo(seg(t,4.9,6.2)))
            a=seg(t,4.8,5.1)*(1-seg(t,8.1,8.4))
            st=textimg(f'{cnt} h',f('black',200),GOLD2); paste_c(fr,st,W/2,560,alpha=a)
            l2=textimg('de motor',f('m',56),WHITE); paste_c(fr,l2,W/2,700,alpha=a)
            for k,(tt,t0) in enumerate([('2024',6.4),('3 lugares',7.0)]):
                s=seg(t,t0,t0+0.35)*(1-seg(t,8.1,8.4))
                if s>0:
                    im=Image.new('RGBA',(440,130),(0,0,0,0)); dd=ImageDraw.Draw(im); pill(dd,220,4,tt,f('xb',58),(16,30,50),WHITE,h=118,outline=GOLD2)
                    paste_c(fr,im,W/2+(-250 if k==0 else 250),1450,scale=0.8+0.2*eob(s),alpha=s)
        # price 8.6-11.6
        if 8.5<=t<11.8:
            a=seg(t,8.6,8.9)*(1-seg(t,11.5,11.8))
            paste_c(fr,T_PRICE,W/2,1330,scale=1+0.5*(1-eob(seg(t,8.6,9.0))),alpha=a)
            s=seg(t,9.4,9.8)*(1-seg(t,11.5,11.8))
            if s>0: paste_c(fr,P18,W/2,1500,scale=0.7+0.3*eob(s),alpha=s)
        # end card
        if t>=11.6:
            e=seg(t,11.6,12.1)
            ov=Image.new('RGBA',(W,H),DEEP+(int(200*e),)); fr.paste(ov,(0,0),ov)
            paste_c(fr,icon(300),W/2,560-40*(1-eo(e)),alpha=e)
            paste_c(fr,T_CTA1,W/2,1000,scale=0.9+0.1*eob(seg(t,12.0,12.4)),alpha=seg(t,12.0,12.3))
            paste_c(fr,T_CTA2,W/2,1110,alpha=seg(t,12.3,12.6))
            paste_c(fr,T_BR,W/2,1500,alpha=seg(t,12.6,13.0))
            pulse=0.5+0.5*math.sin((t-12)*6)
            d=ImageDraw.Draw(fr)
    proc.stdin.write(fr.tobytes())
proc.stdin.close(); proc.wait(); print('done')
