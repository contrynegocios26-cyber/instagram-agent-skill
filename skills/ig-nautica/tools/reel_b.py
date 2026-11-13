import sys,subprocess; sys.path.insert(0,'.')
from kit import *
W,H,FPS=1080,1920,30; DUR=12.0; N=int(DUR*FPS)
def eo(t): t=max(0,min(1,t)); return 1-(1-t)**3
def eio(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def eob(t):
    t=max(0,min(1,t)); c1=1.70158; c3=c1+1; return 1+c3*(t-1)**3+c1*(t-1)**2
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
P=Image.open(U+'bfc748fe-image.jpg').convert('RGB')
P=ImageEnhance.Brightness(P).enhance(1.06); P=ImageEnhance.Contrast(P).enhance(1.12); P=ImageEnhance.Color(P).enhance(1.25)
P=P.resize((1620,2880),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,2)); S=1.5
def view(cx,cy,z):
    w=W/z; h=H/z; cx=min(max(cx,w/2),W-w/2); cy=min(max(cy,h/2),H-h/2)
    box=tuple(int(v*S) for v in (cx-w/2,cy-h/2,cx+w/2,cy+h/2)); return P.crop(box).resize((W,H),Image.BILINEAR)
shots=[(0,2.6,(540,960,1.0),(540,900,1.18)),
       (2.6,5.2,(640,560,1.75),(600,600,1.55)),
       (5.2,7.8,(420,1080,1.45),(470,1040,1.3)),
       (7.8,10.2,(540,880,1.3),(540,960,1.0))]
def cap(fr,lines,t0,t,y=330):
    s=seg(t,t0,t0+0.25)
    if s<=0: return
    d0=ImageDraw.Draw(fr)
    yy=y
    for txt,font,bg,fg in lines:
        w=d0.textlength(txt,font=font); b=d0.textbbox((0,0),txt,font=font); th=b[3]-b[1]
        im=Image.new('RGBA',(int(w+80),th+56),(0,0,0,0)); dd=ImageDraw.Draw(im)
        dd.rounded_rectangle((0,0,im.width-1,im.height-1),radius=22,fill=bg); dd.text((40,28-b[1]),txt,font=font,fill=fg)
        sc=0.6+0.4*eob(s); im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
        fr.paste(im,(int(W/2-im.width/2),int(yy+(th+56)/2-im.height/2)),im); yy+=th+56+18
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
 '-f','lavfi','-t',str(DUR),'-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-c:a','aac','-movflags','+faststart',OUT+'reel-02-loja.mp4'],stdin=subprocess.PIPE)
END=studio(W,H,cy=900)
for i in range(N):
    t=i/FPS
    if t<10.2:
        for a,b,v0,v1 in shots:
            if a<=t<b:
                k=eio(seg(t,a,b)); v=[v0[j]+(v1[j]-v0[j])*k for j in range(3)]; fr=view(*v)
                # quick flash at cut
                if t-a<0.1 and a>0: fr=Image.blend(fr,Image.new('RGB',(W,H),WHITE),0.5*(1-(t-a)/0.1))
                break
        # vignette top for captions
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
        for y in range(700): od.line((0,y,W,y),fill=DEEP+(int(150*(1-y/700)),))
        fr.paste(ov,(0,0),ov)
        if t<2.6: cap(fr,[('Procurando jet ski',f('black',78),WHITE,DEEP),('pro verão?',f('black',78),GOLD,DEEP)],0.0,t)
        elif t<5.2: cap(fr,[('Sea-Doo GTI 2024',f('black',82),WHITE,DEEP),('3 lugares',f('xb',56),NAVY,WHITE)],2.6,t)
        elif t<7.8: cap(fr,[('Só 89 horas',f('black',96),GOLD,DEEP),('de uso',f('xb',60),NAVY,WHITE)],5.2,t)
        else: cap(fr,[('R$ 105 mil',f('black',110),WHITE,DEEP),('em até 18x no cartão',f('xb',58),GOLD,DEEP)],7.8,t)
        fr.paste(icon(90),(W-90-50,H-90-380),icon(90))
    else:
        fr=END.copy(); e=seg(t,10.2,10.6); d=ImageDraw.Draw(fr)
        ic=icon(int(280*(0.8+0.2*eob(e)))); fr.paste(ic,(int(W/2-ic.width/2),int(520-ic.height/2)),ic)
        ctext(d,820,'Seu verão começa aqui.',f('black',78),WHITE)
        if t>10.6: pill(d,W/2,990,'Comente EU QUERO',f('black',66),GOLD,DEEP,h=130)
        if t>10.9: ctext(d,1170,'ou chame no WhatsApp do perfil',f('m',46),MUTE)
        ctext(d,1400,'COUNTRY NEGÓCIOS',f('b',44),GOLD2,sp=10)
    proc.stdin.write(fr.tobytes())
proc.stdin.close(); proc.wait(); print('done')
