import sys
import os
from PIL import Image
import numpy as np
import cv2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "Profile.jpg")
OUT = os.path.join(BASE, "data", "source-prepped.png")

img = Image.open(SRC).convert("RGB")
img = np.array(img)

bg = cv2.createBackgroundSubtractorMOG2()
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
enhanced = clahe.apply(gray)

enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
white = np.full_like(enhanced_rgb, 255)
result = np.where(enhanced_rgb > 180, white, enhanced_rgb)

Image.fromarray(result).save(OUT)
print(f"Saved {OUT}")
