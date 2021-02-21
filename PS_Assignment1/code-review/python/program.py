#!/usr/bin/python

import sys

def Power_Sum(sum, base):
	"""
	input: sum, base
	output: A sequence of powers of the pointed base
	return value: 
	"""
	Power_Sequence = []
	power = 1
	while (sum > 0):
		if (sum % base != 0):
			Power_Sequence.append(power)
		power = power * base  
		sum = int(sum / base)
	
	return Power_Sequence

def main():
	message = ""
	while (message != "q"):
		sum = input("Please enter a natural number: ")
		base = input("Please enter the base: ")
	
		sum = int(sum)
		base = int(base)
	
		Power_Sequence = Power_Sum(sum, base)
		for power in Power_Sequence:
			print(power)
		
		message = input("Do you want to continue: ")
		
	
main()
