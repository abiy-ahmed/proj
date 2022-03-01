import re

with open("squid_access.log","r") as file:
    for line in file:
        data = re.split(r"\s+",line)
        time = data[0]
        elapsed = data[1]
        rhost = data[2]
        code = data[3].split("/")[0]
        status = data[3].split("/")[1]
        sbytes = data[4]
        method = data[5]
        url = data[6]
        user = data[7]
        peer_status = data[8].split("/")[0]
        peer_ip = data[8].split("/")[1]
        stype = data[9]

        if rhost == "192.168.0.224":
            print(url)
        
    
