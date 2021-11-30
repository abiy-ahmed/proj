#this sucks and needs to be updated
import math
rnum = float(input("Input a decimal number: "))
wnum = rnum
base = float(input("Input the new base: "))
digs = float(int(base))
ttl = ""
print("Available digits: "+str(digs))
gloplace = float(0)
glocelldig = float(0)
def cell():
    global wnum
    global base
    global ttl
    global gloplace
    global glocelldig
    place = float(int((math.log(wnum,base))))
    gloplace = place
    print("Current place value: "+str(int(base))+"^"+str(int(place)))
    cell = base*place
    print("Decimal value of place: "+str(cell))
    celldig = float((int(wnum/cell)))
    glocelldig = celldig-1
    print("New base value of place: "+str(celldig))
    wnum = wnum - (cell*celldig)
    print(wnum)
    
if wnum != 0:
    cell()
    ttl = (str(int(glocelldig)))
    print(ttl)
    for x in range(int(gloplace-1)):
           ttl = ttl+"0"
    print(ttl)
if wnum != 0:
    cell()
    ttl = ttl[0:int(gloplace+1)] + str(int(glocelldig))
    for x in range(int(gloplace-1)):
           ttl = ttl+"0"
    print(ttl)
print(ttl)
print(gloplace)
print(ttl[0:int(gloplace+1)])
