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
stockd = ["fish","salt","silk"]
bal = 20
month = ["Ianuarius","Februarius","Martius","Aprilis","Maius","Iunius","Quintilis","Sextilis","September","October","November","December"]
days = [
year = int(261)
def randomize():
    market[0] = random.randint(10,20)
    market[1] = random.randint(50,60)
    market[2] = random.randint(120,140)

def prices():
    print("\nBalance: $"+str(bal))
    print("\nFish: $"+str(market[0])+"   (Owned: "+str(stock[0])+")")
    print("Salt: $"+str(market[1])+"   (Owned: "+str(stock[1])+")")
    print("Silk: $"+str(market[2])+"   (Owned: "+str(stock[1])+")\n")

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
            print("Invalid resource.\n")
            break
def buyamt(res):
    global stockd
    global bal
    capability = int(bal/market[res])
    amount = int(numval("\nHow many?"+" (0-"+str(capability)+")\n~$ "))
    if 0 < amount < 1:
      print("Invalid amount.\n")
      return
    elif amount == 0:
        print("Transaction cancelled.\n")
        return
    if float(amount*market[res]) > bal:
      print("\nYou cannot afford this.\n")
    else:
      stock[res] = stock[res]+amount
      bal = bal-amount*market[res]
      print("\nBought "+str(int(amount))+" "+stockd[res]+" for $"+str(float(amount*market[res]))+". Your balance is now $"+str(float(bal))+".\n")
def sell():
    if (stock[0]+stock[1]+stock[2]) == 0:
        print("You own no resources.\n")
        return
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
            print("Invalid resource.\n")
            return
def checkamt(res):
    global stockd
    global bal
    global stock
    if stock[res] == 0:
        print("You own none of this resource.\n")
        return
    amount = int(numval("\nHow many?"+" (0-"+str(stock[res])+")\n~$ "))
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
    print("What would you like to do? [sleep, market, buy, sell, save, load]")
    action = input("~$ ")
    action = action.lower()
    if action == "sleep":
        day = day+1
        print("\nSleeping...\n")
        time.sleep(1)
        randomize()
        print("Day: "+str(day))
    elif action == "market":
        prices()
    elif action == "buy":
        buy()
    elif action == "sell":
        sell()
    elif action == "save":
        save()
    else:
        print("Invalid action.\n")
