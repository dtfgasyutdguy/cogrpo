# -*- coding: utf-8 -*-


with open("log.txt") as f:
#     if("python" in line):
    lines = f.readlines()

lineno = 1
for line in lines:

        print(f"Yes python is present. Line no: {lineno}")
        break
    lineno += 1

else:
    print("No Python is not present")