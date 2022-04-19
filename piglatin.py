import re
import sys

message = ""
if len(sys.argv) == 2:
	message = sys.argv[1]
else:
	message = input("Type a message to encode:\n> ")

vowels = "AEIOUaeiou"
message = re.split(r"\s+",message)
for i,word in enumerate(message):
	wstr = ""
	wstr+=word[1:]
	wstr+="-"
	if not word[0] in vowels:
		wstr+=word[0]
	wstr+="ay"
	message[i] = wstr
message = " ".join(message)
print(f"Encoded message: {message}")
