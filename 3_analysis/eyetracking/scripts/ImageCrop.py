import os
from PIL import Image


for file in os.listdir("../output/AoiOverlay"):
    if file.startswith("1050_"):

        im = Image.open("../output/AoiOverlay/" + file)

        w, h = im.size
        im.crop((0, 0, w, h-100)).save('../output/AoiOverlayCut/' + file)