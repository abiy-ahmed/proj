from zlib import crc32
import re
from PIL import Image, ImageDraw, ImageColor

IMG_NAME = "out"
IMG_FILETYPE = "png"
BLOCK_HEIGHT = 25
BLOCK_LENGTH = 50

def sstrip(strin): # special strip
	wstrin = ""
	for char in strin:
		if char.isalnum() or char.isspace():
			wstrin+=char
	return wstrin

def remove_empty(li):
	for i,ele in enumerate(li):
		if len(ele) == 0:
			li.pop(i)
	return li

message = input("Enter your plaintext:\n> ").lower()
message = sstrip(message)
words = remove_empty(re.split("\s+",message))
print(f"Plaintext used: \"{message}\"")

im = Image.new("RGB",(BLOCK_LENGTH*2,BLOCK_HEIGHT*len(words)),(0,0,0))
draw = ImageDraw.Draw(im)

for y,word in enumerate(words):
	hash = crc32(word.encode())
	hash = hex(hash)[2:]
	hex_colors = [hash[0:6], hash[6:8]+"0"*4]
	rgb_colors = [ ImageColor.getcolor("#"+hex_colors[0],"RGB") ,ImageColor.getcolor("#"+hex_colors[1],"RGB")]
	print(f"Row {y}: #{hex_colors[0]}, #{hex_colors[1]}\t::\t{rgb_colors[0]},{rgb_colors[1]}")
	for x,color in enumerate(rgb_colors):
		pos = [BLOCK_LENGTH*x,BLOCK_HEIGHT*y]
		draw.rectangle(( pos[0] , pos[1] , pos[0]+BLOCK_LENGTH , pos[1]+BLOCK_HEIGHT ),fill=(color))

im.save(f"{IMG_NAME}.{IMG_FILETYPE}", format=IMG_FILETYPE)
print(f"Saved to {IMG_NAME}.{IMG_FILETYPE}.")
