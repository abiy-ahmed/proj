'''
FAKEDOX 0.0.1

Import handler inspired by https://github.com/AOS-GUI/AOS-GUI
Firefox required
'''

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

while True:    
    try:
        import requests
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from bs4 import BeautifulSoup
    except:
        pipmain(["install","requests"])
        pipmain(["install","selenium"])
        pipmain(["install","bs4"])
    else:
        break

import string
import random
import datetime
import logging
from time import sleep as wait

TOKEN_SET = string.ascii_lowercase+string.ascii_uppercase+"0123456789+/_"
EMAIL_DOMAINS = ["gmail.com","yahoo.com"]
MAC_PREFIXES = ["00:13:CA","00:1C:B3","00:1D:09","00:A0:83","1C:E2:CC","54:9F:13","54:9F:35","74:E2:8C","9C:74:1A","B0:79:08","C8:B5:AD","D4:8F:33","E0:63:E5"]
HEX_SET = "0123456789ABCDEF"
OPTIONS = FirefoxOptions()
OPTIONS.add_argument("-headless")
N_TABS = 2
LOGGING = True

def waitforelement(driver,byvar,byval,timeout=20):
    element = None
    t = 0
    while True:
        if t == timeout:
            return None
        try:
            element = driver.find_element(byvar,byval)
        except:
            t+=1
            wait(1)
            continue
        else:
            break
    return element

def randemail(fname,lname):
    format = random.randint(1,2)
    if format == 1:
        return fname+random.choice([".","_",""])+lname+"@"+random.choice(EMAIL_DOMAINS)
    if format == 2:
        return random.choice([fname,lname])+"".join([str(random.randint(0,9)) for x in range(random.randint(4,6))])+"@"+random.choice(EMAIL_DOMAINS)

def randipv4():
    a = None
    b = None
    while True:
        a = random.randint(11,255)
        b = random.randint(1,255)
        if a == 10:
            continue
        if a == 192 and b == 168:
            continue
        if a == 172 and (b >= 16 and b <= 32):
            continue
        break
    c = random.randint(1,255)
    d = random.randint(1,254)
    return f"{a}.{b}.{c}.{d}"

def randmac():
    address = random.choice(MAC_PREFIXES)
    for x in range(3):
        address += ":"
        for y in range(2):
            address+= random.choice(HEX_SET)
    return address

def randschool(address,age):
    search_term = "school"
    if age >= 18:
        search_term = "university"
    elif age < 18:
        search_term = "high school"
    
    with webdriver.Firefox(options=OPTIONS) as driver:
        driver.get("https://maps.google.com/")
        search_box = waitforelement(driver,By.XPATH,"//input[@id='searchboxinput']")
        search_phrase = f"{search_term} near {address}"
        search_box.send_keys(search_phrase)
        search_button = waitforelement(driver,By.XPATH,"//button[@aria-label='Search']")
        search_button.click()

        first_result = waitforelement(driver,By.XPATH,"//a[@class='hfpxzc']")
        school_name = first_result.get_attribute("aria-label")
        first_result.click()
        
        address_div = waitforelement(driver,By.XPATH,"//button[@class='CsEnBe']")
        school_address = address_div.get_attribute("aria-label").replace("Address: ","")
        return school_name,school_address

def randwork(address):
    with webdriver.Firefox(options=OPTIONS) as driver:
        driver.get("https://maps.google.com/")
        search_box = waitforelement(driver,By.XPATH,"//input[@id='searchboxinput']")
        search_box.send_keys(f"business near {address}")
        search_button = waitforelement(driver,By.XPATH,"//button[@aria-label='Search']")
        search_button.click()

        first_result = waitforelement(driver,By.XPATH,"//a[@class='hfpxzc']")
        work_name = first_result.get_attribute("aria-label")
        first_result.click()
        
        address_div = waitforelement(driver,By.XPATH,"//button[@data-tooltip='Copy address']")
        work_address = None
        if address_div:
            work_address = address_div.get_attribute("aria-label").replace("Address: ","")

        number_div = waitforelement(driver,By.XPATH,"//button[@data-tooltip='Copy phone number']")
        work_number = None
        if number_div:
            work_number = number_div.get_attribute("aria-label").replace("Phone: ","")
        return work_name,work_address,work_number

def randbank(address):
    with webdriver.Firefox(options=OPTIONS) as driver:
        driver.get("https://maps.google.com/")
        search_box = waitforelement(driver,By.XPATH,"//input[@id='searchboxinput']")
        search_phrase = f"bank near {address}"
        search_box.send_keys(search_phrase)
        search_button = waitforelement(driver,By.XPATH,"//button[@aria-label='Search']")
        search_button.click()

        first_result = waitforelement(driver,By.XPATH,"//a[@class='hfpxzc']")
        bank_name = first_result.get_attribute("aria-label")

        return bank_name

def randhc():
    providers = set()
    soup = BeautifulSoup(requests.get("https://www.easyleadz.com/lists/List-of-Health-Care-Companies-in-USA").content,"html.parser")
    for span in soup.find_all("span",{"itemprop":"name"}):
        providers.add(span.text.strip())
    soup = BeautifulSoup(requests.get("https://www.medindia.net/patients/insurance/health-insurance-companies/health-insurance-companies-united-states.htm").content,"html.parser")
    for li in soup.find_all("li",{"class":"list-item"}):
        providers.add(li.find("a").text.strip())
    soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_United_States_insurance_companies").content,"html.parser")
    for li in soup.find_all("ul")[2].find_all("li"):
        providers.add(li.find("a").text.strip())
    return random.choice(list(providers)).capitalize()

def get_longest_key(d):
    return max([len(key) for key in d.keys()])

def display_details(details,discordReadable=False):
    total_spaces = get_longest_key(details)+8
    for key,value in details.items():
        if value == None: continue
        if discordReadable:
            print(key+":"+"**"+" "*(total_spaces-len(key)-1)+"**"+value)
        else:
            print(key+":"+" "*(total_spaces-len(key)-1)+value)

def main():
    logging.basicConfig(level=logging.INFO)
    discname = input("Enter discord username+numbers or leave blank (Ex: John#3668):\n> ")
    discid = None
    disctoken = None
    if len(discname) > 0:
        discid = input("Enter discord ID or leave blank:\n> ")
        if len(discid) == 0:
            discid = ''.join([str(random.randint(0,9)) for x in range(18)])
        logging.info("Generating token...")
        disctoken = ''.join([random.choice(TOKEN_SET) for x in range(24)]) +"."+ ''.join([random.choice(TOKEN_SET) for x in range(6)]) +"."+ ''.join([random.choice(TOKEN_SET) for x in range(38)])
    else:
        discname = None

    gender = None
    while not gender:
        choice = input("Enter gender (Or leave blank)[M/f]:\n> ").lower().strip()
        if choice == "m" or choice == "male" or len(choice) == 0:
            gender = "m"
        elif choice == "f" or choice == "f":
            gender = "f"
        else:
            print("ERROR: Incorrect choice. Try again.")
    fname = None
    fnameurl = "https://namecensus.com/first-names/common-male-first-names/"
    if gender == "f":
        fnameurl = "https://namecensus.com/first-names/common-female-first-names/"
    logging.info("Generating first name...")
    soup = BeautifulSoup(requests.get(fnameurl).content,"html.parser")
    namediv = random.choice(soup.find("div",{"class":"table-expand"}).find("table").find("tbody").find_all("tr"))
    if namediv:
        fname = namediv.find_all("td")[1].text.capitalize()
    
    logging.info("Generating last name...")
    lname = None
    lnameurl = "https://listophile.com/names/last/common/"
    soup = BeautifulSoup(requests.get(lnameurl).content,"html.parser")
    lname = random.choice(soup.find("ol").find_all("li")).text.capitalize()

    logging.info("Generating email...")
    email = randemail(fname.lower(),lname.lower())

    logging.info("Generating address...")
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

    age = None
    while not age:
        choice = input("Enter age or leave blank(Ex: 18):\n> ").strip()
        if len(choice) == 0:
            choice = "18"
        try:
            age = int(choice)
        except:
            print("ERROR: Invalid choice")
    logging.info("Generating DOB...")
    dob = datetime.date.today() - datetime.timedelta(age*365) + datetime.timedelta(days=random.randint(0,364))
    dob = dob.strftime("%m/%d/%Y")

    logging.info("Generating computer addressing...")
    ipv4 = randipv4()
    mac = randmac()
    logging.info("Generating school...")
    school,schooladdr = randschool(address,age)
    work,workaddr,worknum = None,None,None
    if age >= 17:
        logging.info("Generating work...")
        work,workaddr,worknum = randwork(address)
    logging.info("Generating SSN...")
    ssn = str(random.randint(100,999))+"-"+str(random.randint(10,99))+"-"+str(random.randint(1000,9999))
    logging.info("Generating bank info...")
    bank = randbank(address)
    aba = None
    accountnum = None
    if bank:
        aba = str(random.randint(100000000,999999999))
        accountnum = str(random.randint(1000000000,9999999999))
    logging.info("Generating card info...")
    cardnum = str(random.randint(1000,9999))+" "+str(random.randint(1000,9999))+" "+str(random.randint(1000,9999))+" "+str(random.randint(1000,9999))
    exp_date = datetime.date.today() + datetime.timedelta(365*random.randint(1,3)) + datetime.timedelta(30*random.randint(2,6))
    exp_date = exp_date.strftime("%m/%Y")[:3] + exp_date.strftime("%m/%Y")[-2:]
    cvv = str(random.randint(1,999)).rjust(3,"0")

    logging.info("Generating healthcare provider...")
    healthcare = randhc()

    details = {
        "USERNAME":discname,
        "ID":discid,
        "SESSION TOKEN":disctoken,
        "NAME":fname+" "+lname,
        "EMAIL":email,
        "PHONE #":phone_number,
        "ADDRESS":address,
        "DOB":dob,
        "PUBLIC IPV4":ipv4,
        "MAC ADDRESS":mac,
        "SCHOOL":school,
        "SCHOOL ADDRESS":schooladdr,
        "WORK":work,
        "WORK ADDRESS":workaddr,
        "WORK #":worknum,
        "SSN":ssn,
        "BANK":bank,
        "ROUTING #":aba,
        "ACCOUNT #":accountnum,
        "CARD #":cardnum,
        "EXP. DATE":exp_date,
        "CVV":cvv,
        "HEALTHCARE PROVIDER":healthcare
    }
    
    while True:
        display_details(details)
        choice = input("Add/edit/delete entries or leave blank [Ex: 'NAME:None']:\n> ").strip().split(":")
        print(choice)
        if len(choice) != 2:
            break
        key = choice[0].upper()
        value = choice[1]
        if value == "None":
            details[key] = None
        else:
            details[key] = choice[1]

if __name__ == "__main__":
    main()
