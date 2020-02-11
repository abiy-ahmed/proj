import time
import random

place = ["  ","  ","  ","  ","  ","  ","  ","  ","  "]
content = ["X","O"]
pieces = ["  ","  "]            #pieces[0] is user, pieces[1] is bot
def board():
    print(place[0]+" | "+place[1]+" | "+place[2])
    print("-"*10)
    print(place[3]+" | "+place[4]+" | "+place[5])
    print("-"*10)
    print(place[6]+" | "+place[7]+" | "+place[8])

def validateXO(q):
    global content
    while True:
        x = input(q)
        if x.upper() in content:
            return x
        else:
            print("Invalid input.\n")

def userMove():
    print()

def botMove():
    print()
    
def initialize():
    global pieces
    choice = validateXO("Would you like to be X's or O's?\n~$ ")
    choice = choice.upper()
    if choice == "X":
        pieces[0] = "X"
        pieces[1] = "O"
        print("Piece chosen: X\nAI piece: O\n")
    elif choice == "O":
        pieces[0] = "O"
        pieces[1] = "X"
        print("Piece chosen: O\nAI piece: X\n")
    print("Flipping coin", end="")
    time.sleep(1)
    print(".", end="")
    time.sleep(1)
    print(".", end="")
    time.sleep(1)
    print(".")
    time.sleep(1)
    
while True:
    initialize()
    


    
                
    
