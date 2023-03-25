from time import sleep as wait
import random
import requests
from bs4 import BeautifulSoup

signatures = [b'\x1bLua', b'%!PS-Adobe-3.1 EPSF-3.0', b'NES\x1a', b'0\x82', b'%PDF-', b'ITSF\x03\x00\x00\x00`\x00\x00\x00', b'vhdxfile', b'070707', b'MThd', b'IsZ!', b'#EXTM3U', b'MSWIM\x00\x00\x00\xd0\x00\x00\x00\x00', b'x\x01', b'\xff\xd8\xff\xdb', b'Received:', b'Cr24', b'#?RADIANCE\n', b'BZh', b'\x00\x00\x00\x0cjP  \r\n\x87\n', b'e\x87xV', b'{\\rtf1', b'0&\xb2u\x8ef\xcf\x11\xa6\xd9\x00\xaa\x00b\xcel', b'`\xea', b':)\n', b'bvx2', b'IWAD', b'\x1aE\xdf\xa3', b'dex\n035\x00', b'Creative Voice File\x1a\x1a\x00', b'\x00asm', b'M<\xb2\xa1', b'8BPS', b'\xfd7zXZ\x00', b'\n\r\r\n', b'\x00\x00\x01\xb3', b'\xed\xab\xee\xdb', b'\x80*_\xd7', b'Rar!\x1a\x07\x01\x00', b'SQLite format 3\x00', b'regf', b'v/1\x01', b'%!PS', b'\xc9', b'ORC', b'BPG\xfb', b'\rDOC', b'!BDN', b"7z\xbc\xaf'\x1c", b'icns', b'.snd', b'LZIP', b'fLaC', b'\x1f\xa0', b'#!AMR', b'wOFF', b'\x00', b'SEQ6', b'OggS', b'Obj\x01', b'UU\xaa\xaa', b'SDPX', b'\xff\xd8\xff\xe0', b'<?xml ', b'\x0e\xfe\xff', b'\xca\xfe\xba\xbe', b'ER\x02\x00\x00\x00', b'GIF87a', b'book\x00\x00\x00\x00mark\x00\x00\x00\x00', b'wOF2', b'FLIF', b'BLENDER', b'SIMPLE  =                    T', b'\x00\x01\x00\x00Standard ACE DB', b'\xd7\xcd\xc6\x9a', b'/* XPM */', b'ISc(', b'\xa02A\xa0\xa0\xa0', b'II*\x00\x10\x00\x00\x00CR', b'4\x12\xaaU', b'-----BEGIN CERTIFICATE-----', b'\x00\x00\x01\xba', b'!<arch>\n', b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', b'\xa03D\xa0\xa0', b'C64 CARTRIDGE   ', b'\x00\x01\x00\x00Standard Jet DB', b'PMCC', b'ID3', b'-----BEGIN CERTIFICATE REQUEST-----', b'xar!', b'gimp xcf', b'OTTO', b'\x06\x0e+4\x02\x05\x01\x01\r\x01\x02\x01\x01\x02', b'\x04"M\x18', b'G', b'\x06\x06\xed\xf5\xd8\x1dF\xe5\xbd1\xef\xe7\xfet\xb7\x1d', b'II*\x00', b'(\xb5/\xfd']

# def populate_signatures():
#     signatures = dict()
#     site = requests.get("https://en.wikipedia.org/wiki/List_of_file_signatures").content
#     soup = BeautifulSoup(site,"html.parser")
#     table = soup.find("table",{"class":"wikitable"})
#     tbody = table.find("tbody")
#     tr_list = tbody.find_all("tr")
#     tr_list.pop(0)
#     for tr in tr_list:
#         td_list = tr.find_all("td")
#         if len(td_list) < 4: continue
#         try:
#             hex_sig = td_list[0].find("code").text.strip().replace(" ","").replace("?","0")
#             hex_sig = bytes.fromhex(hex_sig)
#             #offset = int(td_list[2].text.strip())
#             #if offset != 0: continue
#             #hex_sig = b"\x00"*offset + hex_sig            
#             extension = td_list[3].text.strip()
#             signatures[extension] = hex_sig
#         finally:
#             continue
#     return signatures

def main():
    # import subprocess
    # sigsthatwork = set()
    # for signature in signatures.values():
    #     with open("schizotest","w") as testfile:
    #         testfile.write("")
    #     with open("schizotest","wb") as testfile:
    #         testfile.write(signature)
    #     filedesc = subprocess.run(["file","-b","schizotest"],capture_output=True,text=True).stdout.strip()
    #     if filedesc == "ASCII text" or filedesc == "ASCII text, with no line terminators" or filedesc == "data":
    #         continue
    #     else:
    #         sigsthatwork.add(signature)
    original = b''
    with open(__file__,"rb") as source:
        original+=source.read()
    try:
        while True:
            with open(__file__,"w") as source:
                source.write("")
            with open(__file__,"wb") as source:
                magic_bytes = random.choice(signatures)
                source.write(magic_bytes)
            wait(0.5)
    finally:
        with open(__file__,"w") as source:
            source.write("")
        with open(__file__,"wb") as source:
            source.write(original)

if __name__ == "__main__":
    main()