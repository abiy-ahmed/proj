import requests
from bs4 import BeautifulSoup
import string
import random

#Discord username (Provided)
    #Discord ID
    #Discord token (24,6,38) base64
#First/Last/Middle Initial
#Email
#Address
#Phone Number (area code depends on fake address)
#DOB/Age (Age range provided)
#Public IPv4
#Public IPv6
#MAC Address
#School (Depends on address and age)
    #School email
#Place of work (Depends on address)
    #Work number
#SSN
#Bank:
#Debit card number:
    #Exp. date
    #CVV
#Request to add or replace custom fields

TOKEN_SET = string.ascii_lowercase+string.ascii_uppercase+"0123456789+/_"
EMAIL_DOMAINS = ["gmail.com","yahoo.com"]

def randemail(fname,lname):
    format = random.randint(1,2)
    if format == 1:
        return fname+random.choice([".","_",""])+lname+"@"+random.choice(EMAIL_DOMAINS)
    if format == 2:
        return random.choice([fname,lname])+"".join([str(random.randint(0,9)) for x in range(random.randint(4,6))])+"@"+random.choice(EMAIL_DOMAINS)

def main():
    discname = input("Enter discord username+numbers or leave blank (Ex: John#3668):\n> ")
    discid = None
    disctoken = None
    if len(discname) > 0:
        discid = input("Enter discord ID or leave blank:\n> ")
        if len(discid) == 0:
            discid = ''.join([str(random.randint(0,9)) for x in range(18)])
        disctoken = ''.join([random.choice(TOKEN_SET) for x in range(24)]) +"."+ ''.join([random.choice(TOKEN_SET) for x in range(6)]) +"."+ ''.join([random.choice(TOKEN_SET) for x in range(38)])
    else:
        discname = None

    gender = None
    while not gender:
        choice = input("Enter gender: [M/f]:\n> ").lower().strip()
        if choice == "m" or choice == "male":
            gender = "m"
        elif choice == "f" or choice == "f":
            gender = "f"
        else:
            print("ERROR: Incorrect choice. Try again.")
    fname = None
    fnameurl = "https://namecensus.com/first-names/common-male-first-names/"
    if gender == "f":
        fnameurl = "https://namecensus.com/first-names/common-female-first-names/"
    soup = BeautifulSoup(requests.get(fnameurl).content,"html.parser")
    namediv = random.choice(soup.find("div",{"class":"table-expand"}).find("table").find("tbody").find_all("tr"))
    if namediv:
        fname = namediv.find_all("td")[1].text.capitalize()
    
    lname = None
    lnameurl = "https://listophile.com/names/last/common/"
    soup = BeautifulSoup(requests.get(lnameurl).content,"html.parser")
    lname = random.choice(soup.find("ol").find_all("li")).text.capitalize()

    email = randemail(fname.lower(),lname.lower())

    phone_number = None
    street = None
    city = None
    state = None
    zip_code = None
    address = None
    addressurl = "https://www.bestrandoms.com/random-address"
    soup = BeautifulSoup(requests.get(addressurl).content,"html.parser")
    addressdiv = soup.find("li",{"class":"col-sm-6 col-md-4"}).find_all("span")
    phone_number = addressdiv[0].text
    street = addressdiv[1].text
    city = addressdiv[2].text
    state = addressdiv[3].text[-3:-1]
    zip_code = addressdiv[4].text
    address = f"{street}, {city}, {state} {zip_code}"

    age_range = None
    while not age_range:
        choice = input("Enter age range(Ex: 18-24):\n> ").strip()
        try:
            age_range = ( int(choice[0:2]) , int(choice[-3:-1]) )
        except:
            print("ERROR: Invalid choice")
    



    if discname: print(f"Username: {discname}")
    if discid: print(f"ID: {discid}")
    if disctoken: print(f"Session token: {disctoken}")
    if fname and lname: print(f"Name: {fname} {lname}")
    if email: print(f"Email: {email}")
    if phone_number: print(phone_number)
    if address: print(address)




if __name__ == "__main__":
    main()