import os
from os import path as p

def move():
    path = "img/icnoutput/"
    os.system(f"mv icon.icns {path}")

    os.system(f"cp -r {path} ../icnoutput")