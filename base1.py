num = float(input("A number in decimal: "))
base = float(input("Provide a new base: "))
r = float(0)
product = ""
print("Calculating...")
while num >= 1:
    num = float(num/base)
    r = num%base
    product = product+str(int(r))
if 0 < num < base:
    product = product+"."
while 0 < num < base:
    num = float(num/base)
    r = num%base
    product = product+str(int(r))
print(product)
