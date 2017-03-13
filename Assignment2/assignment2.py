#!/usr/bin/python

import os
import string
from unidecode import unidecode
import binascii
import random
import time

def pickRandomCoeffs(k):
    # Create a list of 'k' random values.
    randList = []
    m = 2**32 - 1
    while k > 0:
    # Get a random shingle ID.
        randIndex = random.randint(0, m) 
  
    # Ensure that each random number is unique.
        while randIndex in randList:
            randIndex = random.randint(0, m) 
    
    # Add the random number to the list.
        randList.append(randIndex)
        k = k - 1
    
    return randList

n = [2,3]
data = []
shingleInDoc = set()
docsAsShingles2 = []
docsAsShingles3 = []
docsAsShingles2words = []
files = os.listdir('/Users/udaymidha/Documents/COSC5110-datamining/Assignment-2/files')
for file1 in files:
	with open('/Users/udaymidha/Documents/COSC5110-datamining/Assignment-2/files/' + file1, 'r') as f:
		data.append(unidecode(f.read().decode('utf8')).translate(None, string.punctuation).replace('\n',''))	

# 2-gram
for i in range(0, len(data)):
	shingleInDoc = set()
	for j in range(0, len(data[i]) - 2 + 1):
		shingle = data[i][j] + data[i][j + 1]
		crc = binascii.crc32(shingle) & 0xffffffff		
		shingleInDoc.add(crc)
	docsAsShingles2.append(shingleInDoc)

i  = 1
for k in docsAsShingles2:
	print "D" + str(i),len(k)
	i += 1

# 3-gram
for i in range(0, len(data)):
	shingleInDoc = set()
	for j in range(0, len(data[i]) - 3 + 1):
		shingle = data[i][j] + data[i][j + 1] + data[i][j + 2]
		crc = binascii.crc32(shingle) & 0xffffffff
		shingleInDoc.add(crc)
	docsAsShingles3.append(shingleInDoc)

i = 1
for k in docsAsShingles3:
	print "D" + str(i), len(k)
	i += 1


# 2-gram as words
for i in range(0,len(data)):
	shingleInDoc = set()
	words = data[i].split(" ")
	for index in range(0, len(words) - 1):
		shingle = words[index] + words[index + 1]
		crc = binascii.crc32(shingle) & 0xffffffff
		shingleInDoc.add(crc)
	docsAsShingles2words.append(shingleInDoc)

i = 1
for k in docsAsShingles2words:
	print "D" + str(i), len(k)
	i += 1

for i in range(0,len(docsAsShingles2)):
	for j in range(i+1, len(docsAsShingles2)):
		s1 = docsAsShingles2[i]
		s2 = docsAsShingles2[j]
		print "D" + str(i + 1) + " - D" + str(j + 1), len(s1.intersection(s2))/float(len(s1.union(s2)))

for i in range(0,len(docsAsShingles3)):
	for j in range(i+1, len(docsAsShingles3)):
		s1 = docsAsShingles3[i]
		s2 = docsAsShingles3[j]
		print "D" + str(i+1) + " - D" + str(j+1), len(s1.intersection(s2))/float(len(s1.union(s2)))

for i in range(0,len(docsAsShingles2words)):
	for j in range(i+1, len(docsAsShingles2words)):
		s1 = docsAsShingles2words[i]
		s2 = docsAsShingles2words[j]
		print "D" + str(i+1) + "- D" + str(j+1), len(s1.intersection(s2))/float(len(s1.union(s2))) 

################################################
numHashesList = [10, 20, 60, 200, 500]
for numHashes in numHashesList:	
	t0 = time.time()
	prime = 4294967311

	coeff_alpha = pickRandomCoeffs(numHashes)

	signatures = []

	for shingleSet in docsAsShingles3[0:2]:
		signature = []
		for i in range(0, numHashes):
			minHashCode = prime + 1
			for shingleId in shingleSet:
				hashCode = (coeff_alpha[i]*shingleId + 1) % prime
			
				if hashCode < minHashCode:
					minHashCode = hashCode

			signature.append(minHashCode)
		signatures.append(signature)
	
	signature1 = signatures[0]
	signature2 = signatures[1]
	count = 0
	for i in range(0, numHashes):
		count = count + (signature1[i] == signature2[i])

	estJSim = count /float(numHashes)
	time1 = time.time() - t0
	print numHashes, "-",  estJSim, "time:", time1

#################################################
