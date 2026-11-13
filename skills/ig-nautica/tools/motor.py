# Motor de Reels com narração (Piper) + legenda palavra por palavra
import sys,subprocess,wave,os,math,numpy as np; sys.path.insert(0,'.')
from country import *
PY='/tmp/claude-0/rbenv/bin/python'; VD='/tmp/claude-0/voices/'; TMP='/tmp/claude-0/narr/'; os.makedirs(TMP,exist_ok=True)
W,H,FPS,SR=1080,1920,30,22050
def tts(text,voice='faber',ls=0.88):
    out=TMP+f'tts_{abs(hash((text,voice,ls)))}.wav'
    if not os.path.exists(out):
        subprocess.run([PY,'-m','piper','-m',VD+f'pt_BR-{voice}-medium.onnx','-f',out,'--length-scale',str(ls),'--sentence-silence','0.12'],input=text.encode(),check=True,stderr=subprocess.DEVNULL)
    with wave.open(out) as w: x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
    nz=np.where(np.abs(x)>300)[0]; x=x[max(0,nz[0]-200):nz[-1]+800]
    return x.astype(np.float32)/32768
def eo(t): t=max(0,min(1,t)); return 1-(1-t)**3
def eio(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def eob(t):
    t=max(0,min(1,t)); c1=1.70158; c3=c1+1; return 1+c3*(t-1)**3+c1*(t-1)**2
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
CF=wide(56,850)
def caption(fr,t,timed,y):
    act=[x for x in timed if x[4]<=t<x[5]]
    if not act: return
    ws=act[0][3]; cur=[x for x in act if x[0]<=t<x[1]]; wi=cur[0][2] if cur else len(ws)-1
    d=ImageDraw.Draw(fr); sp=d.textlength(' ',font=CF)+24
    chs=[]; cur_=[]; wsum=0
    for k,w in enumerate(ws):
        wl=d.textlength(w,font=CF)
        if cur_ and (len(cur_)>=3 or wsum+sp+wl>940): chs.append(cur_); cur_=[]; wsum=0
        wsum+= (sp if cur_ else 0)+wl; cur_.append(k)
    chs.append(cur_); ch=[c for c in chs if wi in c][0]; wd=[d.textlength(ws[k],font=CF) for k in ch]; x=W/2-(sum(wd)+sp*(len(ch)-1))/2
    for k,w_ in zip(ch,wd):
        if k==wi: d.rounded_rectangle((x-14,y-12,x+w_+14,y+78),radius=16,fill=GOLD); d.text((x,y),ws[k],font=CF,fill=NAVY2)
        else: d.text((x,y),ws[k],font=CF,fill=WHITE,stroke_width=7,stroke_fill=(10,16,28))
        x+=w_+sp
def build(scenes,out,ycap=1040,voice='faber'):
    """scenes: dict(spk, cap, draw(fr_or_None,t,dur)->Image, min=0, pad=0.45, lead=0.15)"""
    auds=[]; T=0; timed=[]; spans=[]
    for s in scenes:
        x=tts(s['spk'],voice) if s.get('spk') else np.zeros(1,np.float32); sd=len(x)/SR
        lead=s.get('lead',0.15); dur=max(s.get('min',0),lead+sd+s.get('pad',0.45))
        auds.append((T+lead,x)); spans.append((T,dur))
        if s.get('cap'):
            ws=s['cap'].split(); L=[len(w)+2 for w in ws]; tot=sum(L); t=T+lead
            for i,l in enumerate(L): dd=sd*l/tot; timed.append((t,t+dd,i,ws,T+lead,T+lead+sd+0.25)); t+=dd
        T+=dur
    track=np.zeros(int(T*SR)+SR,np.float32)
    for st,x in auds: i=int(st*SR); track[i:i+len(x)]+=x
    track=track[:int(T*SR)]; track=track/max(1e-6,np.abs(track).max())*0.9
    wav=out+'.wav'
    with wave.open(wav,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((track*32767).astype(np.int16).tobytes())
    wr=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',wav,
      '-af','highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5,aresample=44100','-ac','2',
      '-c:v','libx264','-pix_fmt','yuv420p','-crf','19','-preset','medium','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
    N=int(T*FPS)
    for i in range(N):
        t=i/FPS
        for s,(a,d) in zip(scenes,spans):
            if a<=t<a+d: fr=s['draw'](t-a,d); break
        else: fr=scenes[-1]['draw'](spans[-1][1],spans[-1][1])
        if (t-a)<0.08 and a>0 and s.get('flash',True): fr=Image.blend(fr,Image.new('RGB',(W,H),WHITE),0.4*(1-(t-a)/0.08))
        caption(fr,t,timed,s.get('ycap',ycap)); wr.stdin.write(fr.tobytes())
    wr.stdin.close(); wr.wait(); os.remove(wav); return T
