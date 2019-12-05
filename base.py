import math
rnum = float(input("Input a decimal number: "))
wnum = rnum
base = float(input("Input the new base: "))
digs = float(int(base))
ttl = ""
print("Available digits: "+str(digs))

def cell():
    global wnum
    global base
    global ttl
    place = float(int((math.log(wnum,base))))
    print("Current place value: "+str(int(base))+"^"+str(int(place)))
    cell = base*place
    print("Decimal value of place: "+str(cell))
    celldig = float((int(wnum/cell)))
    wnum = wnum - (cell*celldig)
    print(wnum)
    
if wnum != 0:
    
