from zlib import crc32
import re
from PIL import Image, ImageDraw, ImageColor
from math import floor
import subprocess

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

def check_exists(filename):
	if len(filename) == 0 or filename.isspace():
		print("ERROR: no filename provided")
		exit()
	try:
		open(filename,"r").close()
	except:
		print("ERROR: file not found")
		exit()

def encode():
	message = input("Enter your plaintext:\n> ").lower()
	message = sstrip(message)
	if len(message) == 0:
		print("ERROR: valid message not provided.")
		exit()
	words = remove_empty(re.split("\s+",message))
	if not words or len(words) == 0:
		print("ERROR: no message provided.")
		exit()
	print(f"Plaintext used: \"{message}\"")

	im = Image.new("RGB",(BLOCK_LENGTH*2,BLOCK_HEIGHT*len(words)),(0,0,0))
	draw = ImageDraw.Draw(im)

	for y,word in enumerate(words):
		hash = crc32(word.encode())
		hash = hex(hash)[2:].zfill(8)
		hex_colors = [hash[0:6], hash[6:8]+"0"*4]
		rgb_colors = [ ImageColor.getcolor("#"+hex_colors[0],"RGB") ,ImageColor.getcolor("#"+hex_colors[1],"RGB")]
		print(f"Row {y}: Hash: {hash}\t::\tHex: #{hex_colors[0]}, #{hex_colors[1]}\t::\tRGB: {rgb_colors[0]},{rgb_colors[1]}")
		for x,color in enumerate(rgb_colors):
			pos = [BLOCK_LENGTH*x,BLOCK_HEIGHT*y]
			draw.rectangle(( pos[0] , pos[1] , pos[0]+BLOCK_LENGTH , pos[1]+BLOCK_HEIGHT ),fill=(color))

	im.save(f"{IMG_NAME}.{IMG_FILETYPE}", format=IMG_FILETYPE)
	print(f"Saved to {IMG_NAME}.{IMG_FILETYPE}.")

def decode():
	img_name = input("Enter the name of the image to decode:\n> ")
	try:
		Image.open(img_name)
	except:
		print("ERROR: Image not found.")
		exit()

	hashfile_name = input("Enter the name of the resulting hash file: (WARNING: EXISTING FILE WILL BE OVERWRITTEN)\n> ")
	if len(hashfile_name) == 0 or hashfile_name.isspace():
		print("ERROR: no name provided")
		exit()
	open(hashfile_name,"w").close()

	img = Image.open(img_name)
	img.convert("RGB")
	img_width,img_height = img.size

	with open(hashfile_name,"a") as file:
		for y in range(int(img_height/BLOCK_HEIGHT)):
			hash = ""
			for x in (0,1):
				x_ = BLOCK_LENGTH*x+floor(BLOCK_LENGTH/2)
				y_ = BLOCK_HEIGHT*y+floor(BLOCK_HEIGHT/2)
				for cval in img.getpixel((x_,y_)):
					hash+=hex(cval)[2:].zfill(2)
			hash = hash[:8]+":"+"0"*8
			print(hash)
			file.write(hash+"\n")
	print(f"command:\nhashcat -a 0 -m 11500 {hashfile_name} <wordlist> && hashcat -m 11500 {hashfile_name} --show > results.txt")

def map():
	message = ""

	hashfile_name = input("Enter the name of your hashfile:\n> ").strip()
	check_exists(hashfile_name)
	hashcat_output_name = input("Enter the name of the hashcat output file:\n> ").strip()
	check_exists(hashcat_output_name)

	with open(hashfile_name,"r") as hashfile:
		for hash in hashfile:
			if len(hash) < 17:
				continue
			found = False
			with open(hashcat_output_name) as hashcat_output:
				for line in hashcat_output:
					if len(line) < 17:
						continue
					if hash[0:17] == line[0:17]:
						found = True
						message+=line.split(":")[2].strip()+" "
			if not found:
				message += "(?) "
	print("\n-----BEGIN PLAINTEXT-----")
	print(message)
	print("-----END PLAINTEXT-----\n")

choice = input("encode, decode, or map?\n> ").lower().strip()
if choice == "decode":
	decode()
elif choice == "encode":
	encode()
elif choice == "map":
	map()
else:
	print("Invalid choice.")
	exit()
