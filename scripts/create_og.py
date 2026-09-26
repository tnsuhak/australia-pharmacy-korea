"""Deterministic social card, using project typography; not a webpage screenshot."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1]
font=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'assets/NotoSansKR-subset.ttf'
def f(size,weight=600):
 face=ImageFont.truetype(str(font),size)
 try:face.set_variation_by_axes([weight])
 except (OSError,AttributeError):pass
 return face
im=Image.new('RGB',(1200,630),'#f1f6ed');d=ImageDraw.Draw(im)
d.text((74,62),'AUSTRALIA PHARMACY GUIDE',font=f(17,650),fill='#006b64')
d.polygon([(938,54),(960,76),(938,98),(916,76)],fill='#ddb33c');d.text((924,66),'TNS',font=f(11,800),fill='white')
d.text((978,59),'호주약대 가이드',font=f(19,700),fill='#183d41')
d.text((70,148),'2027 호주 약대 비교',font=f(69,750),fill='#183d41')
d.text((70,245),'나에게 맞는 입학경로부터.',font=f(64,750),fill='#006b64')
d.text((75,361),'학력 · 선수과목 · 영어 · 학비 · 약사등록',font=f(25,450),fill='#536d6c')
x=75
for word in ['Direct','Foundation','Diploma','Graduate Entry']:
 width=d.textlength(word,font=f(18,600))+36
 d.rounded_rectangle((x,435,x+width,481),radius=8,fill='white',outline='#bdd0c4',width=1)
 d.text((x+18,443),word,font=f(18,600),fill='#183d41');x+=width+12
d.text((75,540),'TNS · 2027 AUSTRALIAN PHARMACY PATHWAYS',font=f(14,550),fill='#627c70')
d.rectangle((0,615,1200,630),fill='#006b64')
im.save(ROOT/'assets/og-image.png',optimize=True)
print('Created assets/og-image.png · 1200×630')
