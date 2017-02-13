#!/usr/bin/python
from __future__ import division
import BitVector
import math

x = 9
approx = 0
for i in range(0, 250):
	b = BitVector.BitVector(intVal = x**i)
	a = BitVector.BitVector( intVal = math.factorial(i))
	approx = approx + b.intValue()/a.intValue()

approx = 1/approx
expected = math.exp(-x)
print "%.20f"%(approx)
print (abs(approx - expected)*100)/expected

