import sys,subprocess,numpy as np; sys.path.insert(0,'.')
from country import *
W,H,FPS=1080,1920,30
D='/home/user/instagram-agent-skill/midia/2026-11-13-gti-2024/country/'
SCRIPTS={
 'reel-01-89-horas':[(3.3,4.8,'Sea-Doo GTI 2024.'),(5.0,8.2,'Só 89 horas de motor, modelo 2024, três lugares.'),
                     (8.7,11.4,'R$ 105 mil, ou em até 18 vezes no cartão.'),(11.9,14.7,'Comente EU QUERO ou chama no WhatsApp.')],
 'reel-02-loja':[(0.3,2.8,'Procurando jet ski pro verão?'),(3.1,5.6,'Olha esse Sea-Doo GTI 2024.'),(5.9,8.4,'Só 89 horas de uso, três lugares.'),
                 (8.7,11.0,'R$ 105 mil, ou em até 18 vezes no cartão.'),(11.3,12.9,'Chama no WhatsApp da Country!')],
}
YCAP={'reel-01-89-horas':1060,'reel-02-loja':1000}
def words_timed(lines):
    out=[]
    for a,b,txt in lines:
        ws=txt.split(); L=[len(w)+2 for w in ws]; T=sum(L); t=a; chunk=[]
        for i,(w,l) in enumerate(zip(ws,L)):
            d=(b-a)*l/T; out.append((t,t+d,w,a,b,i,ws)); t+=d
    return out
FONT=wide(62,850)
def chunks(ws,n=3):
    return [list(range(i,min(i+n,len(ws)))) for i in range(0,len(ws),n)]
def draw(fr,t,timed,y):
    cur=[x for x in timed if x[3]<=t<x[4]]
    if not cur: return
    line=cur[0]; ws=line[6]; idx=[x for x in cur if x[0]<=t<x[1]]
    wi=idx[0][5] if idx else len(ws)-1
    ch=[c for c in chunks(ws) if wi in c][0]
    d=ImageDraw.Draw(fr); sp=d.textlength(' ',font=FONT)+24
    widths=[d.textlength(ws[k],font=FONT) for k in ch]; tot=sum(widths)+sp*(len(ch)-1); x=W/2-tot/2
    for k,w_ in zip(ch,widths):
        if k==wi:
            d.rounded_rectangle((x-14,y-12,x+w_+14,y+80),radius=16,fill=GOLD)
            d.text((x,y),ws[k],font=FONT,fill=NAVY2)
        else:
            d.text((x,y),ws[k],font=FONT,fill=WHITE,stroke_width=7,stroke_fill=(10,16,28))
        x+=w_+sp
for name,lines in SCRIPTS.items():
    src=D+name+'.mp4'; dst=D+name+'-legendado.mp4'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    rd=subprocess.Popen(['ffmpeg','-loglevel','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    wr=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
      '-f','lavfi','-t',str(dur),'-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-movflags','+faststart',dst],stdin=subprocess.PIPE)
    timed=words_timed(lines); i=0
    while True:
        buf=rd.stdout.read(W*H*3)
        if len(buf)<W*H*3: break
        fr=Image.frombytes('RGB',(W,H),buf); draw(fr,i/FPS,timed,YCAP[name]); wr.stdin.write(fr.tobytes()); i+=1
    wr.stdin.close(); wr.wait(); print(name,i)
