import os
import subprocess
import re
from time import sleep as wait

def write_message(username,message):
    message+="\n"
    read, write = os.pipe()
    os.write(write, message.encode("utf-8"))
    os.close(write)
    subprocess.run(["write",username],stdin=read)

def kick_terminal(terminal_name):
    ps_output = subprocess.run(["ps","-ft",terminal_name],capture_output=True,text=True).stdout.strip().split("\n")
    line = re.split(r"\s+",ps_output[1])
    pid = line[1]
    subprocess.run(["sudo","kill","-9",pid])

#Inspired by NCAE competition
#Display list of terminals and the user that's logged in
subprocess.run(["sudo","echo"])
w_output = subprocess.run(["w","-h"],capture_output=True,text=True).stdout.strip().split("\n")
whoami = subprocess.run(["whoami"],capture_output=True,text=True).stdout.strip()
sessions = list()
for i,line in enumerate(w_output):
    line = re.split(r"\s+",line)
    session = {
        "username":line[0],
        "tty":line[1],
        "ip":line[2],
    }
    if session["username"] == whoami or session["tty"]==":0":
        continue
    else:
        sessions.append(session)

if len(sessions) == 0:
    print("No other sessions found. Exiting...")
    exit()

#Prompt user to choose a terminal
session_choice = None
selected = False
while not selected:
    print("Please select a terminal...")
    for session in sessions:
        print(f"{session['tty']}\t\t{session['username']}\t\t{session['ip']}")
    choice = input("> ").strip()
    for session in sessions:
        if choice == session["tty"]:
            session_choice = session
            selected = True
    if not selected:
        print(f"Error: {choice} is not a terminal...\n")

#Choose first, between rock, paper or scissors
choice = ""
valid_choices = ("rock","paper","scissors")
while True:
    choice = input("Choose rock, paper, or scissors...\n> ").lower().strip()
    if choice in valid_choices:
        break
    else:
        print(f"Error: {choice} is not a valid choice.\n")

subprocess.run(["mkdir","/tmp/rps"],stderr=subprocess.DEVNULL)
subprocess.run(["rm","-f","/tmp/rps/rock"],stderr=subprocess.DEVNULL)
subprocess.run(["rm","-f","/tmp/rps/paper"],stderr=subprocess.DEVNULL)
subprocess.run(["rm","-f","/tmp/rps/scissors"],stderr=subprocess.DEVNULL)
subprocess.run(["chmod","777","/tmp/rps"],stderr=subprocess.DEVNULL)
#subprocess.run(["script","-f","out"])
print("Awaiting opponent's choice...")
#Write to target user's terminal "Choose rock, paper, or scissors" and store their choice
write_message(session_choice["username"],"Choose rock, paper, or scissors...\n\(ex: touch /tmp/rps/rock\)")
opponent_choice = None
while not opponent_choice:
    for c in valid_choices:
        if os.path.exists(f"/tmp/rps/{c}"):
            opponent_choice = c
            break
    wait(0.2)
#Write to both terminals "Rock..." "Paper..." "Scissors..." "Shoot!" and show each user's choice
print("Rock...")
write_message(session_choice["username"],"Rock...")
wait(1)
print("Paper...")
write_message(session_choice["username"],"Paper...")
wait(1)
print("Scissors...")
write_message(session_choice["username"],"Scissors...")
wait(1)
print("Shoot!")
write_message(session_choice["username"],"Shoot!")
print(f"You chose:\t{choice}")
print(f"{session_choice['username']} chose:\t{opponent_choice}")
write_message(session_choice["username"],f"You chose:\t{opponent_choice}\n{whoami} chose:\t{choice}")
condition = None
if choice == opponent_choice:
    condition = "draw"
elif choice == "rock" and opponent_choice == "scissors":
    condition = "win"
elif choice == "paper" and opponent_choice == "rock":
    condition = "win"
elif choice == "scissors" and opponent_choice == "paper":
    condition = "win"
else:
    condition = "lose"

if condition == "draw":
    print("Draw.")
    write_message(session_choice["username"],"Draw.")
elif condition == "win":
    print(f"You win! {session_choice['username']} has been kicked.")
    write_message(session_choice["username"],"You lose. Seeya!")
    kick_terminal(session_choice["tty"])
elif condition == "lose":
    write_message(session_choice["username"],f"You win! {whoami} has been kicked.")
    print("You lose. Seeya!")
    my_terminal_name = subprocess.run(["tty"],capture_output=True,text=True).stdout.strip().replace("/dev/","")
    kick_terminal(my_terminal_name)

#Kill the loser's terminal terminal/use UFW to block that user's IP
