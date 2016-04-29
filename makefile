# Simple makefile to run blender with our testfile and script
#

FILE=dev6.blend

OUTFOLDER=out/
OUT=rattan.png

OUTFILE=$(OUTFOLDER)$(OUT)
export OUTFILE

all: export RENDER=1
all:
	blender $(FILE) --background --python test1.py
	open $(OUTFILE)

open: export RENDER=0
open:
	blender $(FILE) --python test1.py

test:
	echo $(OUTFILE)
