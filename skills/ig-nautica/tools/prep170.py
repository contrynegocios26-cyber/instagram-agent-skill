from PIL import Image, ImageFilter
import numpy as np
U='/root/.claude/uploads/c388b183-f909-530a-9de4-4ce57692aac2/19d4c0f4-image.jpg'
J=Image.open('/tmp/claude-0/j170_final.png'); OFF=(72,214)
# soften paper patch
reg=(408-72-6,350-214-6,508-72+6,377-214+6); p=J.crop(reg).filter(ImageFilter.GaussianBlur(2.5)); J.paste(p,reg[:2]); J.save('/tmp/claude-0/j170_final.png')
P=np.array(Image.open(U).convert('RGB')).astype(float)
c0=np.array(Image.open('/tmp/claude-0/cut170.png'))[...,3]
F=np.zeros(c0.shape); F[OFF[1]:OFF[1]+J.height,OFF[0]:OFF[0]+J.width]=np.array(J)[...,3]
hole=(c0>60)&(F<128); hole[420:]=False
hole=np.array(Image.fromarray((hole*255).astype('uint8')).filter(ImageFilter.MaxFilter(15)))>0
X=P.copy(); X[hole]=P[~hole].mean(0)
for _ in range(250):
    B=np.array(Image.fromarray(X.astype('uint8')).filter(ImageFilter.BoxBlur(4))).astype(float); X[hole]=B[hole]
im=Image.fromarray(np.clip(X,0,255).astype('uint8')); im.paste(J,OFF,J); im.save('/tmp/claude-0/photo170_clean.jpg',quality=95); print('ok')
