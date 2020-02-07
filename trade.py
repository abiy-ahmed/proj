import time
import random
def numval(q):
    while True:
        try:
            x = float(input(q))
            return x
        except:
            print("Please input a valid number.")

market = [0, 0, 0]
stock = [0, 0, 0]
bal = 20
def randomize():
    market[0] = random.randint(10,20)
    market[1] = random.randint(50,60)
    market[2] = random.randint(120,140)

def prices():
    print("\nFish: $"+str(market[0]))
    print("Salt: $"+str(market[1]))
    print("Silk: $"+str(market[2])+"\n")

def owned():
    print("\nFish owned: "+str(stock[0]))
    print("Salt owned: "+str(stock[1]))
    print("Silk owned: "+str(stock[2])+"\n")

def buy():  
    choice = input("\nWhat would you like to buy? [Fish, Salt, Silk]\n~$ ")
    choice = choice.lower()
    while True:
        if choice == "fish":
            buyamt(0)
            break
        elif choice == "salt":
            buyamt(1)
            break
        elif choice == "silk":
            buyamt(2)
            break
        else:
            print("Select a valid resource.")
def buyamt(res):
    stockd = ["fish","salt","silk"]
    global bal
    amount = int(numval("\nHow many?\n~$ "))
    if amount < 1:
      print("Invalid amount.\n")
      return
    if float(amount*market[res]) > bal:
      print("\nYou cannot afford this.\n")
    else:
      stock[res] = stock[res]+amount
      bal = bal-amount*market[res]
      print("\nBought "+str(int(amount))+" "+stockd[res]+" for $"+str(float(amount*market[res]))+". Your balance is now $"+str(float(bal))+".\n")
def sell():  
    choice = input("\nWhat would you like to sell? [Fish, Salt, Silk]\n~$ ")
    choice = choice.lower()
    while True:
        if choice == "fish":
            checkamt(0)
            break
        elif choice == "salt":
            checkamt(1)
            break
        elif choice == "silk":
            checkamt(2)
            break
        else:
            print("Select a valid resource.")
def checkamt(res):
    stockd = ["fish","salt","silk"]
    global bal
    global stock
    amount = int(numval("\nHow many?\n~$ "))
    if amount > stock[res]:
      print("Insufficient stock.")
    else:
      stock[res] = stock[res]-amount
      bal = bal+amount*market[res]
      print("\nSold "+str(amount)+" "+stockd[res]+" for $"+str(float(amount*market[res]))+". Your balance is now $"+str(float(bal))+".\n")
randomize()
day = 1
print("Day: 1")
print("Balance: $20")
while True:
    print("What would you like to do? [sleep, prices, buy, sell, stock, balance]")
    action = input("~$ ")
    action = action.lower()
    if action == "sleep":
        day = day+1
        print("\nSleeping...\n")
        time.sleep(3)
        randomize()
        print("Day: "+str(day))
    elif action == "prices":
        prices()
    elif action == "stock":
        owned()
    elif action == "buy":
        buy()
    elif action == "balance":
       print("\nBalance: $"+str(bal)+"\n")
    elif action == "sell":
        sell()
