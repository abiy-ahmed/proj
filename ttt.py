import time
import random
import datetime
import hashlib

place = [" "," "," "," "," "," "," "," "," "]
content = ["X","O"]
coin = 0
pieces = {"user":" ","bot":" "}
playername = " "
gamestart = " "
gamestart1 = " "
prehash = "F"

def template():
    print(" 1 | 2 | 3")
    print(" "+"-"*10)
    print(" 4 | 5 | 6")
    print(" "+"-"*10)
    print(" 7 | 8 | 9\n") 
    
def board():
    print("\n "+place[0]+" | "+place[1]+" | "+place[2])
    print(" "+"-"*10)
    print(" "+place[3]+" | "+place[4]+" | "+place[5])
    print(" "+"-"*10)
    print(" "+place[6]+" | "+place[7]+" | "+place[8]+"\n")

def validatePlace(q):
    while True:
        try:
            x = int(input(q))
            while True:
                if x in range(1,10):
                    return x
                else:
                    print("Invalid number.")
                    break
        except:
            print("Please input a valid number.")

def validateXO(q):
    global content
    while True:
        x = input(q)
        if x.upper() in content:
            return x
        else:
            print("Invalid input.\n")

def userMove():
    global prehash
    while True:
        placechoice = (validatePlace("Where would you like to mark? (1-9)\n~$ ")-1)
        if place[placechoice] == " ":
            place[placechoice] = pieces["user"]
            break
        else:
            print("Place already taken.\n")
    prehash = prehash+"U"+str(placechoice)
    moveBuffer("user")

def botMove():
    global prehash
    print("AI is deciding", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".")
    time.sleep(0.7)
    while True:
        placechoice = random.randint(0,8)
        if place[placechoice] == " ":
            place[placechoice] = pieces["bot"]
            break
    prehash = prehash+"B"+str(placechoice)
    moveBuffer("bot")

def moveBuffer(last):
    board()
    checkWin(last)
    checkStale()
    if last == "user":
        botMove()
    elif last == "bot":
        userMove()

def checkWin(player):
    global place
    global pieces
    global prehash
    comb = [place[0]+place[1]+place[2], place[3]+place[4]+place[5], place[6]+place[7]+place[8], place[0]+place[3]+place[6], place[1]+place[4]+place[7], place[2]+place[5]+place[8], place[0]+place[4]+place[8], place[2]+place[4]+place[6]]
    for x in comb:
        if x == str(pieces[player]*3):
            if player == "user":
                print("You have won!")
                prehash = prehash+"WU"
                time.sleep(1)
                resolve("u")
            elif player == "bot":
                print("The AI has won.")
                prehash = prehash+"WU"
                time.sleep(1)
                resolve("b")

def checkStale():
    global prehash
    global place
    if " " in place:
        return
    else:
        prehash = prehash+"WS"
        resolve("s")

def resolve(winner):
    global playername
    global gamestart
    global coin
    global pieces
    global content
    global prehash
    gameend = datetime.datetime.now()
    gameendt = time.time()
    bin = ["yes", "no", "y", "n"]
    prehash = prehash+str(random.randint(100,1000))
    checksum = hashlib.md5(prehash.encode())
    checksum = checksum.hexdigest()
    winners = {"u":playername,"b":"The AI",0:playername,1:"The AI","s":"N/A (Stalemate)"}
    if winner == "s":
        print("A stalemate has occurred.")
        time.sleep(1)
    log = open("winlog.txt", "a")
    log.write("-"*40+"\nGame ID: "+str(checksum[:10].upper())+"\nGame start: "+str(gamestart)+"\nGame end: "+str(gameend)+"\nGame duration: "+str(int(gameendt-gamestartt))+" seconds\nWinner: "+winners[winner]+"\nFirst move: "+winners[coin]+"\n"+playername+" piece: "+content[0]+"\nAI piece: "+content[1]+"\nFinal gameboard:\n"+place[0]+" | "+place[1]+" | "+place[2]+"\n"+"-"*10+"\n"+place[3]+" | "+place[4]+" | "+place[5]+"\n"+"-"*10+"\n"+place[6]+" | "+place[7]+" | "+place[8]+"\n"+"-"*40+"\n")
    log.close()
    print("\nSaving results", end="")
    time.sleep(0.7)
    print(".", end="")
    time.sleep(0.7)
    print(".", end="")
    time.sleep(0.7)
    print(".")
    time.sleep(1)
    print("Results saved.\n")
    time.sleep(1)
    while True:
        ask = input("Would you like to play again? [Y/n]\n~$ ")
        ask = ask.lower()
        if ask == "yes" or ask == "y":
            initialize()
        elif ask == "no" or ask == "n":
            print("\nThanks for playing!\n")
            time.sleep(1)
            exit()
        else:
            print("Invalid input.\n")

def initialize():
    global pieces
    global coin
    global place
    global playername
    global gamestart
    global gamestartt
    global prehash
    prehash = "F"
    place = [" "," "," "," "," "," "," "," "," "]
    playername = input("\nChoose a username:\n~$ ")
    choice = validateXO("\nWould you like to be X's or O's? [X/O]\n~$ ")
    choice = choice.upper()
    if choice == "X":
        pieces["user"] = "X"
        pieces["bot"] = "O"
        print("\nPiece chosen: X\nAI piece: O\n")
    elif choice == "O":
        pieces["user"] = "O"
        pieces["bot"] = "X"
        print("\nPiece chosen: O\nAI piece: X\n")
    print("Flipping coin", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".")
    time.sleep(1)
    x = random.randint(0,1)
    if x == 0:
        coin = 0
        print("You will go first.\n")
        prehash = prehash+"U"
        time.sleep(1)
        template()
        time.sleep(0.5)
        gamestart = datetime.datetime.now()
        gamestartt = time.time()
        userMove()
    elif x == 1:
        coin = 1
        print("The AI will go first.\n")
        prehash = prehash+"B"
        time.sleep(1)
        template()
        time.sleep(0.5)
        gamestart = datetime.datetime.now()
        gamestartt = time.time()
        botMove()

initialize()
