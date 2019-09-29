## -*- coding: cp1252 -*-
import os

filePath = "./testFiles/alice29.txt"

file = open(filePath, 'rb')

size = os.path.getsize(filePath)

s = ""
for i in range(size):
    a = file.read(1)
    s += a.decode("iso-8859-1")

print(s)

file.close()

outPath = "./testFiles/bin/alice.txt"
out = open(outPath, "wb")
out.write(s.encode("iso-8859-1"))