'''
Copyright (C) 2023 https://github.com/haile-selassie

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import subprocess
import re
from time import sleep as wait

class Session:
    def __init__(self,username,tty,ip):
        self.username = username
        self.tty = tty
        self.ip = ip
        self.choice = None
    def writeto(self,messageStr):
        messageStr+="\n"
        read, write = os.pipe()
        os.write(write, messageStr.encode("utf-8"))
        os.close(write)
        subprocess.run(["write",self.username],stdin=read)
    def kick(self):
        ps_output = subprocess.run(["ps","-ft",self.tty],capture_output=True,text=True).stdout.strip().split("\n")
        line = re.split(r"\s+",ps_output[1])
        pid = line[1]
        subprocess.run(["sudo","kill","-9",pid])

#Inspired by NCAE competition
#Display list of terminals and the user that's logged in
try:
    subprocess.run(["sudo","echo"],check=True)
except:
    print("ERROR: This script requires sudo privileges in order to run.")
    exit()
w_output = subprocess.run(["w","-h"],capture_output=True,text=True).stdout.strip().split("\n")
whoami = subprocess.run(["whoami"],capture_output=True,text=True).stdout.strip()
sessions = list()
my_session = None
opp_session = None
for i,line in enumerate(w_output):
    line = re.split(r"\s+",line)
    username = line[0]
    tty = line[1]
    ip = line[2]
    if tty == ":0":
        ps_output = subprocess.run([f"ps aux | grep {username} | grep xorg"],shell=True,capture_output=True,text=True).stdout.strip().split("\n")
        line = re.split(r"\s+",ps_output[0])
        xorg_pid = line[1]
        tty = line[6]
    newSession = Session(username,tty,ip)
    if newSession.username == whoami:
        my_session = newSession
    else:
        sessions.append(newSession)

if len(sessions) == 0:
    print("No other sessions found. Exiting...")
    exit()

#Prompt user to choose a terminal
while not opp_session:
    print("Please select a terminal...")
    for session in sessions:
        print(f"{session.tty}\t\t{session.username}\t\t{session.ip}")
    choice = input("> ").strip()
    for session in sessions:
        if choice == session.tty:
            opp_session = session
    if not opp_session:
        print(f"Error: {choice} is not a terminal...\n")

#Choose first, between rock, paper or scissors
valid_choices = ("rock","paper","scissors")
while not my_session.choice:
    choice = input("Choose rock, paper, or scissors...\n> ").lower().strip()
    if choice in valid_choices:
        my_session.choice = choice
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
opp_session.writeto("Choose rock, paper, or scissors...\n\(ex: touch /tmp/rps/rock\)")
while not opp_session.choice:
    for c in valid_choices:
        if os.path.exists(f"/tmp/rps/{c}"):
            opp_session.choice = c
            break
    wait(0.2)
#Write to both terminals "Rock..." "Paper..." "Scissors..." "Shoot!" and show each user's choice
print("Rock...")
opp_session.writeto("Rock...")
wait(1)
print("Paper...")
opp_session.writeto("Paper...")
wait(1)
print("Scissors...")
opp_session.writeto("Scissors...")
wait(1)
print("Shoot!")
opp_session.writeto("Shoot!")
print(f"You chose:\t{my_session.choice}")
print(f"{opp_session.username} chose:\t{opp_session.choice}")
opp_session.writeto(f"You chose:\t{opp_session.choice}\n{my_session.username} chose:\t{my_session.choice}")
condition = None
if my_session.choice == opp_session.choice:
    condition = "draw"
elif my_session.choice == "rock" and opp_session.choice == "scissors":
    condition = "win"
elif my_session.choice == "paper" and opp_session.choice == "rock":
    condition = "win"
elif my_session.choice == "scissors" and opp_session.choice == "paper":
    condition = "win"
else:
    condition = "lose"

if condition == "draw":
    print("Draw.")
    opp_session.writeto("Draw.")
elif condition == "win":
    print(f"You win! {opp_session.username} has been kicked.")
    opp_session.writeto("You lose. Seeya!")
    opp_session.kick()
elif condition == "lose":
    opp_session.writeto(f"You win! {my_session.username} has been kicked.")
    print("You lose. Seeya!")
    my_session.kick()

#Kill the loser's terminal terminal/use UFW to block that user's IP
