import sys,subprocess,wave,os,numpy as np; sys.path.insert(0,'.')
from country import *
VOICE=sys.argv[1] if len(sys.argv)>1 else 'faber'
PY='/tmp/claude-0/rbenv/bin/python'; VD='/tmp/claude-0/voices/'
W,H,FPS=1080,1920,30
D='/home/user/instagram-agent-skill/midia/2026-11-13-gti-2024/country/'
TMP='/tmp/claude-0/narr/'; os.makedirs(TMP,exist_ok=True)
# (inicio, fim máximo, texto falado, texto da legenda ou None)
R={
'reel-01-89-horas':[(0.1,2.7,'Ele tem oitenta e nove horas... e parece zero.',None),
 (2.8,5.05,'Si Dú, gê tê i, dois mil e vinte e quatro.','Sea-Doo GTI 2024.'),
 (5.15,8.45,'Oitenta e nove horas de motor. Três lugares.','89 horas de motor. Três lugares.'),
 (8.6,11.5,'Cento e cinco mil reais, ou em até dezoito vezes no cartão.','R$ 105 mil, ou em até 18x no cartão.'),
 (11.8,14.9,'Comenta eu quero, ou chama a Cântri no zap!','Comente EU QUERO ou chama a Country no zap!')],
'reel-02-loja':[(0.2,2.9,'Procurando jet ski pro verão?','Procurando jet ski pro verão?'),
 (3.0,5.7,'Olha esse Si Dú, gê tê i, dois mil e vinte e quatro.','Olha esse Sea-Doo GTI 2024.'),
 (5.8,8.5,'Só oitenta e nove horas de uso. Três lugares.','Só 89 horas de uso. Três lugares.'),
 (8.6,11.1,'Cento e cinco mil, ou dezoito vezes no cartão.','R$ 105 mil, ou 18x no cartão.'),
 (11.2,12.95,'Chama a Cântri no zap!','Chama a Country no zap!')]}
SR=22050
def tts(text,ls,out):
    subprocess.run([PY,'-m','piper','-m',VD+f'pt_BR-{VOICE}-medium.onnx','-f',out,'--length-scale',str(ls),'--sentence-silence','0.15'],input=text.encode(),check=True,stderr=subprocess.DEVNULL)
    with wave.open(out) as w: return w.getnframes()/w.getframerate()
def trim(out):
    with wave.open(out) as w: sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
    nz=np.where(np.abs(x)>300)[0]; x=x[max(0,nz[0]-200):nz[-1]+800] if len(nz) else x
    return x,sr
FONT=wide(62,850)
def chunks(n,k=3): return [list(range(i,min(i+k,n))) for i in range(0,n,k)]
for name,lines in R.items():
    src=D+name+'.mp4'; dst=D+name+'-narrado.mp4'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    track=np.zeros(int(dur*SR)+SR,dtype=np.float32); timed=[]
    for j,(a,b,spk,cap) in enumerate(lines):
        f=TMP+f'{name}_{j}.wav'; ls=0.88
        for _ in range(4):
            tts(spk,ls,f); x,sr=trim(f); d=len(x)/sr
            if d<=b-a: break
            ls*= (b-a)/d*0.98
        print(name,j,round(d,2),'slot',round(b-a,2),'ls',round(ls,2))
        s=int(a*SR); track[s:s+len(x)]+=x.astype(np.float32)/32768
        if cap:
            ws=cap.split(); L=[len(w)+2 for w in ws]; T=sum(L); t=a
            for i,l in enumerate(L): dd=d*l/T; timed.append((t,t+dd,i,ws,a,a+d+0.25)); t+=dd
    track=track[:int(dur*SR)]; pk=np.abs(track).max(); track=track/pk*0.9
    wav=TMP+name+'.wav'
    with wave.open(wav,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((track*32767).astype(np.int16).tobytes())
    rd=subprocess.Popen(['ffmpeg','-loglevel','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    wr=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',wav,
      '-af','highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5,aresample=44100','-ac','2',
      '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',dst],stdin=subprocess.PIPE)
    y={'reel-01-89-horas':1060,'reel-02-loja':1000}[name]; i=0
    while True:
        buf=rd.stdout.read(W*H*3)
        if len(buf)<W*H*3: break
        t=i/FPS; fr=Image.frombytes('RGB',(W,H),buf)
        act=[x for x in timed if x[4]<=t<x[5]]
        if act:
            ws=act[0][3]; cur=[x for x in act if x[0]<=t<x[1]]; wi=cur[0][2] if cur else len(ws)-1
            ch=[c for c in chunks(len(ws)) if wi in c][0]; d=ImageDraw.Draw(fr); sp=d.textlength(' ',font=FONT)+24
            wd=[d.textlength(ws[k],font=FONT) for k in ch]; x=W/2-(sum(wd)+sp*(len(ch)-1))/2
            for k,w_ in zip(ch,wd):
                if k==wi: d.rounded_rectangle((x-14,y-12,x+w_+14,y+80),radius=16,fill=GOLD); d.text((x,y),ws[k],font=FONT,fill=NAVY2)
                else: d.text((x,y),ws[k],font=FONT,fill=WHITE,stroke_width=7,stroke_fill=(10,16,28))
                x+=w_+sp
        wr.stdin.write(fr.tobytes()); i+=1
    wr.stdin.close(); wr.wait(); print('ok',dst)
