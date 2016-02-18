# Simple makefile to reun blender with our testfile and script
#

all:
	blender dev1.blend --background --python test1.py
	open out/rattan.png

open:
	blender dev1.blend --python test1.py -he
	open out/rattan.png
