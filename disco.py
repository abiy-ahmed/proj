from zlib import crc32
import re
from PIL import Image, ImageDraw, ImageColor
from math import floor, ceil
import subprocess
import os
from shutil import rmtree
from random import randint
import string
from numpy import base_repr
import binwalk

IMG_NAME = "out"
IMG_FILETYPE = "bmp"
BLOCK_HEIGHT = 25
BLOCK_LENGTH = 50
ENCODE_DEPENDENCIES = ("gcc","gzip","head","tail")
EXTRACT_DEPENDENCIES = tuple()
PADDING_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
WORDLIST_LENGTH = 100000
PADDING_RADIUS = 5
SOURCE_FILE_NAME = "disco_temp.c"
BINARY_FILE_NAME = "disco_temp"

# Input dummy phrase
# Include preshared secret in binary compression

def sstrip(strin): # special strip
	wstrin = ""
	for char in strin:
		if char.isalnum() or char.isspace():
			wstrin+=char
	return wstrin

def estrip(strin): # empty strip
	strin = re.split(r"\s+",strin)
	for i,ele in enumerate(strin):
		if len(ele) == 0:
			strin.pop(i)
	return strin

def is_empty(strin):
	if not strin or len(strin) == 0 or strin.isspace():
		return True
	return False

def check_exists(filename):
	try:
		open(filename,"r").close()
	except:
		return False
	return True

def depend_error(programstr):
	print(f"ERROR: dependency \"{programstr}\" is not installed.\ntry \"sudo apt install {programstr}\"")
	exit()

def check_depends(mode):
	depends = None
	if mode == "encode":
		depends = ENCODE_DEPENDENCIES
	elif mode == "extract":
		depends = EXTRACT_DEPENDENCIES
	else:
		print("Error detecting type for check_depends.")
		exit()
	for depend in depends:
		out = subprocess.run(["which",depend],capture_output=True)
		if out.returncode == 1:
			depend_error(depend)

def get_crc32_hash(s):
	hash = crc32(s.encode())
	hash = hex(hash)[2:].zfill(8)
	return hash

def img_from_list(li):
	im = Image.new("RGB",(BLOCK_LENGTH*2,BLOCK_HEIGHT*len(li)),(0,0,0))
	draw = ImageDraw.Draw(im)

	for y,word in enumerate(li):
		hash = get_crc32_hash(word)
		hex_colors = [hash[0:6], hash[6:8]+"0"*4]
		rgb_colors = [ ImageColor.getcolor("#"+hex_colors[0],"RGB") ,ImageColor.getcolor("#"+hex_colors[1],"RGB")]
		print(f"Row {y}: Hash: {hash}\t::\tHex: #{hex_colors[0]}, #{hex_colors[1]}\t::\tRGB: {rgb_colors[0]},{rgb_colors[1]}")
		for x,color in enumerate(rgb_colors):
			pos = [BLOCK_LENGTH*x,BLOCK_HEIGHT*y]
			draw.rectangle(( pos[0] , pos[1] , pos[0]+BLOCK_LENGTH , pos[1]+BLOCK_HEIGHT ),fill=(color))
	return im

def pad(s):
	new = ""
	for c in range(1+PADDING_RADIUS*2):
		if c == PADDING_RADIUS:
			new+=s
		else:
			new+=PADDING_CHARSET[randint(0,len(PADDING_CHARSET)-1)]
	return new

def prog_shift(s,dir):
	new = ""
	for i,char in enumerate(s):
		shift = len(s)-i
		aset = None
		if char.isnumeric():
			new+=char
			continue
		elif char.isupper():
			aset = string.ascii_uppercase
		else:
			aset = string.ascii_lowercase
		aset = list(aset)
		set_i = aset.index(char)
		if dir and dir == "reverse":
			start = ceil(shift/26)*26
			shift = shift*(-1)
			new_index = (start+shift+set_i)%26
			new+=aset[new_index]
		else:
			new_index = (shift+set_i)%26
			new+=aset[new_index]
	return new


def random_encode(s):
	new = ""
	rbase = randint(16,36)
	for char in s:
		new += base_repr(ord(char),base=rbase)
	return new

def random_word():
	wstr = ""
	for i in range(randint(2,9)):
		wstr+=PADDING_CHARSET[randint(0,len(PADDING_CHARSET)-1)]
	return wstr

def encode():
	check_depends("encode")
	message = input("Enter your plaintext:\n> ")
	message = sstrip(message)
	message = estrip(message)

	if not message or len(message) == 0:
		print("ERROR: valid message not provided.")
		exit()

	print(f"Plaintext used: \"{' '.join(message)}\"")

	padded_words = [None]*len(message)
	for i,word in enumerate(message):
		word = pad(word)
		padded_words[i] = word
	print(f"Hash words used: {', '.join(padded_words)}")


	#Generate the image
	img = img_from_list(padded_words)
	img_name = ""
	while True:
		img_name = input("Type the name of the image to be saved:\n> ")
		if is_empty(img_name):
			print("ERROR: no name provided.")
			continue
		elif check_exists(img_name):
			savechoice = input(f"WARNING: {img_name} already exists! Would you like to overwrite it? [Y/n]\n> ").lower()
			if savechoice == "y" or savechoice == "yes":
				break
			elif savechoice == "n" or savechoice == "no":
				print("File not overwritten.")
				continue
			else:
				print("Invalid choice.")
				continue
		else:
			break
	img_name = img_name.strip(f".{IMG_FILETYPE}")
	img.save(f"{img_name}.{IMG_FILETYPE}", format=IMG_FILETYPE)
	print(f"Saved to {IMG_NAME}.{IMG_FILETYPE}.")

	print("Creating wordlist...")
	used = set()
	for word in padded_words:
		used.add(word)
	while len(used) < WORDLIST_LENGTH:
		rand = pad(random_word())
		used.add(rand)
		#rand_line = str(randint(1,10000))
		#head = subprocess.Popen(["head","-n",rand_line,"popular.txt"], stdout=subprocess.PIPE)
		#out = subprocess.check_output(["tail","-n","1"], stdin=head.stdout).decode().rstrip()
		#out = pad(out)
		#used.add(out)

	used = list(used)

	print("Applying shift...")
	#shift here
	order = randint(0,1) # 0 = descending, 1 = ascending
	for i,word in enumerate(used):
		shifted_word =  prog_shift(word,"forward")
		used[i] = shifted_word

	print("Encoding by number base...")
	#random base encode here
	for i,word in enumerate(used):
		based_word = random_encode(word)
		used[i] = based_word

	print("Writing source file...")
	open(SOURCE_FILE_NAME,"w").close()
	with open(SOURCE_FILE_NAME,"a") as sfile:
		sfile.write("#include <stdio.h>\n")
		for word in used:
			sfile.write("int _"+word+"(){return 0;}\n")
		phrase = input("Write a misdirection phrase:\n> ")
		sfile.write("int main(){printf(\""+phrase+"\");return 0;}\n")

	print("Compiling binary...")
	gcc = subprocess.call(["gcc",SOURCE_FILE_NAME,"-o",BINARY_FILE_NAME])

	print("Compressing binary...")
	gzip = subprocess.call(["gzip","-n",BINARY_FILE_NAME])
	print("Embedding binary...")
	with open(f"{img_name}.{IMG_FILETYPE}","ab") as coverfile:
		cat = subprocess.Popen(["cat",f"{BINARY_FILE_NAME}.gz"],stdout=coverfile)
	print("Done!")

def decode_arb_base(s,base):
	wstr = ""
	for i in range(int(len(s)/2)):
		d1 = s[i*2]
		d2 = s[i*2+1]
		pair = d1+d2
		new_int = 0
		try:
			int(pair,base)
		except:
			return None
		new_int = int(pair,base)

		try:
			chr(new_int)
		except:
			return None
		char = chr(new_int)
		if char not in PADDING_CHARSET:
			return None
		wstr+=char
	return wstr

def decode():
	check_depends("extract")
	img_name = input("Enter the name of the image to decode:\n> ")
	try:
		Image.open(img_name)
	except:
		print("ERROR: Image not found.")
		exit()

	img = Image.open(img_name)
	img.convert("RGB")
	img_width,img_height = img.size

	hashpot = list()
	for y in range(int(img_height/BLOCK_HEIGHT)):
		hash = ""
		for x in (0,1):
			x_ = BLOCK_LENGTH*x+floor(BLOCK_LENGTH/2)
			y_ = BLOCK_HEIGHT*y+floor(BLOCK_HEIGHT/2)
			for cval in img.getpixel((x_,y_)):
				hash+=hex(cval)[2:].zfill(2)
		hash = hash[:8]
		hashpot.append(hash)

	print(f"{len(hashpot)} hashes found.")
	print("\n".join(hashpot))

	print("Extracting binary...")
	extract_dir_name = f"_{img_name}.extracted"
	if os.path.isdir(extract_dir_name): rmtree(extract_dir_name)

	modules = binwalk.scan(img_name,signature=True,extract=True,quiet=True)
	offset = modules[0].results[1].offset
	name = hex(offset).upper()[2:]
	strings = subprocess.run(["strings",f"{extract_dir_name}/{name}"],capture_output=True).stdout.decode().split("\n")

	numlist = list()
	for line in strings:
		line = line.rstrip()
		if len(line) > 1 and len and line[1:].isalnum() and len(line[1:])%2==0:
			numlist.append(line[1:])

	print(f"{len(numlist)} possible words found.")
	print("Bruteforcing number bases...")
	wordlist = list()
	for word in numlist:
		for base in range(16,36):
			decoded = decode_arb_base(word,base)
			if decoded:
				wordlist.append(decoded)
	print(f"Created wordlist with {len(wordlist)} lines.")

	print("Reversing shift...")
	for i,word in enumerate(wordlist):
		shifted = prog_shift(word,"reverse")
		wordlist[i] = shifted

	print("Cracking hashes...")
	for i,hash in enumerate(hashpot):
		found = False
		for word in wordlist:
			new_hash = get_crc32_hash(word)
			if new_hash == hash:
				hashpot[i] = word[5:-5]
				found = True
		if not found: hashpot[i] = "(?)"

	print("-----BEGIN PLAINTEXT MESSAGE-----")
	print(" ".join(hashpot))
	print("-----END PLAINTEXT MESSAGE-----")

choice = input("encode or decode?\n> ").lower().strip()
if choice == "decode":
	decode()
elif choice == "encode":
	encode()
else:
	print("Invalid choice.")
	exit()
