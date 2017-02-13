#!/usr/bin/python
import math
x = 9
No_of_terms = 28
approx = 0
for i in range(0,No_of_terms):
    approx = approx + math.pow(x,i)/math.factorial(i)
approx = 1/approx
error = (abs(approx - math.exp(-1*x))*100)/math.exp(-1*x)
print "Approximation = %r"%approx
print "Error = %r"%error



## Uncomment to calculate the number of terms required to get an error less the 1*10^-5
"""
import math
x = 9
No_of_terms = 1
approx = 0
error = 100
while error > 1 * 10**-5:
	for i in range(0,No_of_terms):
		approx = approx + math.pow(x,i)/math.factorial(i)
	approx = 1/approx
	error = (abs(approx - math.exp(-1*x))*100)/math.exp(-1*x)
	No_of_terms += 1
print No_of_terms - 1
"""
