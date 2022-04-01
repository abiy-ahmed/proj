from struct import *
import sys
from datetime import datetime

sep = "\t|\t"

def bytes_to_ip(bytes):
    ip = ""
    for b in bytes:
        ip+=str(b)+"."
    return ip[:len(ip)-1]

with open("cap.sky","rb") as file:
    byte_data = file.read()
    magic_bytes = byte_data[0:8]
    version = byte_data[8:9]
    creation_timestamp = byte_data[9:13]
    secret_byte = byte_data[13:14]
    flag_length = int.from_bytes(byte_data[14:18],byteorder="big")
    flag = byte_data[18:(18+flag_length)]

    print(f"Version: {version.hex()}")
    print("Creation timestamp: ",end="")
    print(int.from_bytes(creation_timestamp,byteorder="big"))
    print(f"Secret byte: {secret_byte.hex()}")
    print(f"Flag length: {str(flag_length)}")
    print(f"Flag: {flag.hex()}")

    i = 18+flag_length
    n = 1
    
    entries = int.from_bytes(byte_data[i:(i+4)],byteorder="big")
    i+=4
    for n in range(0,entries):
        src_ip = bytes_to_ip(byte_data[i:(i+4)])
        i+=4

        dst_ip = bytes_to_ip(byte_data[i:(i+4)])
        i+=4

        src_port = byte_data[i:(i+4)]
        i+=4

        dst_port = byte_data[i:(i+4)]
        i+=4

        timestamp = byte_data[i:(i+4)]
        i+=4
        datetimestamp = str(datetime.fromtimestamp(int.from_bytes(timestamp,byteorder="big")).date())

        print(f"Packet {str(n+1):}",end=sep)
        print(f"Src IP: {src_ip}",end=sep)
        print(f"Dest IP: {dst_ip}",end=sep)
        print(f"Src Port: ",end="")
        print(int.from_bytes(src_port,byteorder="big"),end=sep)
        print(f"Dest Port: ",end="")
        print(int.from_bytes(dst_port,byteorder="big"),end=sep)
        print("Time: ",end="")
        #print(int.from_bytes(timestamp,byteorder="big"))
        print(datetimestamp)