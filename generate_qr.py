import sys
sys.path.insert(0, "/tmp/fish-coin-python")
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
from pathlib import Path

URL = "https://glmorris1.github.io/fish-on-the-line/"
OUT = Path("assets")
OUT.mkdir(exist_ok=True)

qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=24, border=4)
qr.add_data(URL)
qr.make(fit=True)
matrix = qr.get_matrix()
n = len(matrix)
qr.make_image(fill_color="black", back_color="white").save(OUT/"qr-control.png")
S = 24
NAVY = "#062838"
TEAL = "#087581"
WHITE = "#f8f1df"

im = Image.new("RGB", (n*S, n*S), WHITE)
d = ImageDraw.Draw(im)

def finder_cell(r,c):
    # Preserve each 7x7 finder plus its one-module separator untouched.
    for rr,cc in ((4,4),(4,n-11),(n-11,4)):
        if rr-1 <= r <= rr+7 and cc-1 <= c <= cc+7: return True
    return False

def art_color(r,c):
    # Recolor only existing dark modules to reveal a fish, tail, line and splash.
    x,y=(c+.5)*S,(r+.5)*S
    fish=((x-(cx if 'cx' in globals() else n*S/2))/105)**2 + ((y-(cy if 'cy' in globals() else n*S/2))/48)**2 <= 1
    tail=(cx-170 < x < cx-88 and abs(y-cy) < (x-(cx-180))*.55) if 'cx' in globals() else False
    line=(abs(x-cx-12)<18 and cy-175<y<cy-42) if 'cx' in globals() else False
    splash=(cy+45<y<cy+135 and abs(x-cx)<220 and ((r+c)%3==0)) if 'cy' in globals() else False
    return TEAL if fish or tail or line or splash else NAVY

cx,cy=(n*S)//2,(n*S)//2
for r,row in enumerate(matrix):
    for c,on in enumerate(row):
        if not on: continue
        x,y=c*S,r*S
        color = NAVY if finder_cell(r,c) else art_color(r,c)
        d.rectangle((x,y,x+S-1,y+S-1),fill=color)

im.save(OUT/"fish-qr.png",dpi=(600,600))

# SVG master embeds exact module geometry and the same restrained center art.
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n*S} {n*S}">',f'<rect width="100%" height="100%" fill="{WHITE}"/>']
for r,row in enumerate(matrix):
    for c,on in enumerate(row):
        if on:
            color=NAVY if finder_cell(r,c) else art_color(r,c)
            svg.append(f'<rect x="{c*S}" y="{r*S}" width="{S}" height="{S}" fill="{color}"/>')
svg += ['</svg>']
(OUT/"fish-qr.svg").write_text("".join(svg))
print(URL, n, im.size)
