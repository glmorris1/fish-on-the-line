import sys
sys.path.insert(0, "/tmp/fish-coin-python")
from PIL import Image, ImageEnhance, ImageFilter

base = Image.open("assets/coin-base.png").convert("RGB")
qr = Image.open("assets/fish-qr.png").convert("RGB")

# Keep every QR module on an integer pixel grid in the nearly orthographic inset.
qr = qr.resize((490, 490), Image.Resampling.NEAREST)

# A tiny contrast reduction makes the printed enamel sit naturally in the scene
# while preserving a high scan contrast ratio.
qr = ImageEnhance.Contrast(qr).enhance(0.96)
base.paste(qr, (382, 333))
base.save("assets/fish-coin-mockup.png", quality=96)
