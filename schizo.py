from time import sleep as wait
import random
import requests
from bs4 import BeautifulSoup

def populate_signatures():
    signatures = dict()
    site = requests.get("https://en.wikipedia.org/wiki/List_of_file_signatures").content
    soup = BeautifulSoup(site,"html.parser")
    table = soup.find("table",{"class":"wikitable"})
    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")
    tr_list.pop(0)
    for tr in tr_list:
        td_list = tr.find_all("td")
        if len(td_list) < 4: continue
        try:
            hex_sig = td_list[0].find("code").text.strip().replace(" ","").replace("?","0")
            hex_sig = bytes.fromhex(hex_sig)
            #offset = int(td_list[2].text.strip())
            #if offset != 0: continue
            #hex_sig = b"\x00"*offset + hex_sig            
            extension = td_list[3].text.strip()
            signatures[extension] = hex_sig
        finally:
            continue
    return signatures

def main():
    original = b''
    signatures = populate_signatures()
    with open(__file__,"rb") as source:
        original+=source.read()
    try:
        while True:
            with open(__file__,"w") as source:
                source.write("")
            with open(__file__,"wb") as source:
                magic_bytes = random.choice(list(signatures.values()))
                source.write(magic_bytes)
            wait(0.5)
    finally:
        with open(__file__,"w") as source:
            source.write("")
        with open(__file__,"wb") as source:
            source.write(original)

if __name__ == "__main__":
    main()