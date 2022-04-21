import re
import sys

message = ""

def help():
	print(f"\nUsage: {sys.argv[0]} COMMAND [MESSAGE]\n")
	print("Commands:")
	print("\tencode")
	print("\tdecode")
	print("\t-h, --help")
	exit()

if len(sys.argv) < 2:
	print("ERROR: missing command")
	help()

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
	help()

if sys.argv[1] not in ("encode","decode"):
	print(f"ERROR: unknown command \"{sys.argv[1]}\"")
	help()

if len(sys.argv) >= 3:
	message = sys.argv[len(sys.argv)-1]
else:
	message = input(f"Type a message to {sys.argv[1]}:\n> ")

if len(message) == 0:
	print("ERROR: must provide message.")
	exit()

message = re.split(r"\s+",message.strip())

if len(message[0]) == 0:
	print("ERROR: must provide message.")
	exit()

def encode(msg):
	for i,word in enumerate(msg):
		word = word.strip().lower()
		wstr = ""

		punc = re.search(r"[?!.,]*$",word)
		if punc:
			wstr+=word[1:punc.span()[0]]
		else:
			wstr+=word[1:]

		wstr+="-"
		if not word[0] in "Aa":
			wstr+=word[0]
		wstr+="ay"

		if punc:
			wstr+=punc.group()
		message[i] = wstr
	return " ".join(msg).capitalize()

def decode(msg):
	for i,word in enumerate(msg):
		word = word.lower()
		wstr = ""
		suffix = re.search(r"-\w?ay",word)
		if not suffix:
			continue
		elif len(suffix.group()) == 4:
			wstr+= suffix.group()[1]
		elif len(suffix.group()) == 3:
			wstr+="a"
		wstr+= word[0:suffix.span()[0]]
		wstr+= word[suffix.span()[1]:]
		msg[i] = wstr
	return " ".join(msg).capitalize()


if sys.argv[1] == "encode":
	message = encode(message)
	print(message)
elif sys.argv[1] == "decode":
	message = decode(message)
	print(message)
else:
	print("ERROR: something went wrong.")
	exit()
