import os
import random
#Graphic template
r'''
|______
|     |
|     O
|    /|\
|    / \
|
=========
'''
filename = "phrases.txt"
save_filename = "hangmanresults.txt"
default_phrases = (
        "No life without love",
        "Let there be light",
        "Beg the question",
        "Free Hong Kong",
        "Life finds a way",
        "Hello World",
    )
hangmen = (
    "|______\n|     |\n|\n|\n|\n|\n=========",
    "|______\n|     |\n|     O\n|\n|\n|\n=========",
    "|______\n|     |\n|     O\n|     |\n|\n|\n=========",
    "|______\n|     |\n|     O\n|    /|\n|\n|\n=========",
    "|______\n|     |\n|     O\n|    /|\\\n|\n|\n=========",
    "|______\n|     |\n|     O\n|    /|\\\n|    /\n|\n=========",
    "|______\n|     |\n|     O\n|    /|\\\n|    / \\\n|\n========="
)
phrases = default_phrases
banned_characters = r"1234567890~!@#$%^&*()_+[]\;',./{}|:<>?"

def make_first_file():
    with open(filename, "w") as file: file.write("")
    with open(filename, "a") as file:
        file.write("CUSTOM no\n")
        for phrase in default_phrases:
            file.write(f"{phrase}\n")

def load_custom_file():
    global phrases
    with open(filename,"r") as file:
        for line in file:
            for char in line:
                if char in banned_characters or char == '"':
                    print(f"Invalid character detected: {char} in phrase {line}\nGoing with default...")
                    return
        file.seek(0)
        phrases = list()
        for line in file:
            if "CUSTOM" not in line:
                phrases.append(line)

def check_for_custom_file():
    if not os.path.exists(filename):
        return make_first_file()
    with open(filename,"r") as file:
        if file.readlines()[0].rstrip() != "CUSTOM yes": return
    while True:
        choice = str(input("Custom file detected! Would you like to use it? [Y/n]\n$ ")).lower()
        if choice == "y" or choice == "yes":
            return load_custom_file()
        elif choice == "n" or choice == "no":
            return
        else: print("Invalid option.\n")

def random_phrase_from_file():
    return random.choice(phrases).rstrip()

def get_letters(str):
    letters = ""
    for letter in str:
        if letter not in letters and letter.isalpha():
            letters += letter.lower()
    return "".join(sorted(letters))

def save_items(*things):
    with open(save_filename,"a") as file:
        for x in things: file.write(f"{x}\n")
    print("Saved.")

class Hangman():
    def __init__(self,name):
        self.Username = name
        self.Health = 6
        self.Phrase = random_phrase_from_file()
        self.CorrectLetters = get_letters(self.Phrase)
        self.GuessedLetters = ""
        self.Board = ""
    def Update(self):
        graphic = hangmen[self.Health]
        shadow = list(''.join(self.Phrase))
        for i,char in enumerate(shadow):
            wasupper = char.isupper()
            char = char.lower()
            if char.isalpha() and char not in self.GuessedLetters:
                shadow[i] = "_"
            if wasupper == True: char.upper()
        shadow = ''.join(shadow)
        self.Board = f"{graphic}\n{shadow}    Guessed: {self.GuessedLetters.upper()}"
    def Draw(self):
        print(self.Board)
    def Damage(self):
        self.Health -= 1
        print("Lost a limb!\n")
    def Guess(self,letter):
        letter = letter.lower()
        if letter in self.GuessedLetters:
            print("Already guessed.\n")
            return
        else:
            self.GuessedLetters += letter
        if letter not in self.CorrectLetters: self.Damage()
    def CheckEnd(self):
        #Check for win
        n = 0
        for x in self.GuessedLetters:
            if x in self.CorrectLetters: n += 1
        if n == len(self.CorrectLetters): return "won"

        #Check for loss
        if self.Health <= 0:
            print(f"The answer was: {self.Phrase}")
            return "lost"
        return None
    def Resolve(self,won):
        while True:
            choice = str(input(f"You have {won}! Would you like to save? [Y/n]\n$ ")).lower()
            if choice == "y" or choice == "yes":
                save_items(f"Player: {self.Username}",self.Board,self.Phrase,"\n<>\n")
                break
            elif choice == "n" or choice == "no":
                break
            else:
                print("Invalid input.\n")
        return


def init():
    print("Welcome to hangman!")
    name = str(input("What is your name?\n$ "))
    game = Hangman(name)
    while True:
        game.Update()
        game.Draw()
        solve = game.CheckEnd()
        if solve: return game.Resolve(solve)
        while True:
            choice = str(input("Guess a letter:\n$ ")).lower()
            if choice.isalpha() and len(choice) == 1: break
            elif not choice.isalpha(): print("Error: Not a letter.\n")
            elif len(choice) > 1: print("Error: Too many letters!.\n")
            else: print("Error: Invalid input.\n")
        game.Guess(choice)

check_for_custom_file()
while True:
    init()
    while True:
        choice = str(input("Would you like to play again? [Y/n]\n$ ")).lower()
        if choice == "y" or choice == "yes":
            break
        elif choice == "n" or choice == "no":
            print("Thank you for playing!!")
            exit()
        else: print("Invalid input.\n")