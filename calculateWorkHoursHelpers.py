import re
import csv
from offsets import Offsets

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 7:24 PM 2024

@author: sebastiendevilliers
"""

def parseInput(inputLine):
	if inputLine:
		return [
			[int(inputLine[1]), # clock in hr
			int(inputLine[2])], # clock in mins
			[int(inputLine[4]), # clock out hr
			int(inputLine[5])] # clock out mins
		]
	return None

def getTimeStamp(hourOffset, clockReading):
	"""Ensures that the value returned is greater than prevTimeStamp by adding 12hrs if it is not"""
	hrsSinceMidnight = clockReading[0] + clockReading[1]/60
	return hrsSinceMidnight + hourOffset

def getData(hourOffsets, clockReadings):
	"""Returns the clockIn and clockOut hours since midnight and the interval between the two in hours"""
	clockIn = getTimeStamp(hourOffsets[0], clockReadings[0])
	clockOut = getTimeStamp(hourOffsets[1], clockReadings[1])

	return (clockIn, clockOut, clockOut - clockIn)

AM = Offsets("am")
NOON = Offsets("noon")
PM = Offsets("pm")
MIDNIGHT = Offsets("midnight")

def calculate(print, input):
	instructions = """
	Please provide the path to your CSV file containing punch-in punch-out times in the following format:

		^([0-9]?[0-9]):([0-9][0-9]) ([0-9]?[0-9]):([0-9][0-9])$

	Each line in the CSV file should contain one entry, e.g.:

		8:00 12:00
		1:00 5:00
	"""
	print(instructions)

	file_path = input("Enter the path to your CSV file: ")

	clockedInHours = 0
	oldClockOut = 0
	hourOffsets = AM.offsets # Allows us to track am (+0hr) vs pm (+12hr)

	try:
		with open(file_path, newline='') as csvfile:
			csv_reader = csv.reader(csvfile)
			next(csv_reader, None) # skip header
			clockReadings, parsedDate, parsedHourOffsets = parseInput(next(csv_reader, None))

			while clockReadings:
				clockIn, clockOut, interval = getData(hourOffsets, clockReadings)

				if oldClockOut <= clockIn and clockIn <= clockOut:
					clockedInHours += interval
				else:
					switchOffsets = {
						NOON.key: ,
					}
					if hourOffsets == PM_OFFSETS:
						input(f"Damn, you're working late! Looks like you worked from {clockReadings[0]}:{clockReadings[1]}pm on . Press Enter to continue.")
						print(f"\nInvalid timestamps entered, calculation stopped.\nHours worked before erroneous data: {round(clockedInHours, 2)}\nPlease try again.\n")
						clockIn, clockOut, interval, oldClockOut, clockedInHours = 0,0,0,0,0
						noonFlag = "am"
					else:
						# fix issue
						noonFlag = "pm" if oldClockOut > clockIn else "in-between"
						clockIn, clockOut, interval = getData(noonFlag, clockReadings)

						# check that it's fixed
						if oldClockOut > clockIn or clockIn > clockOut:
							print(f"\nCalculation stopped due to invalid timestamps.\nHours worked before erroneous data: {round(clockedInHours, 2)}\nPlease try again.\n")
							clockIn, clockOut, interval, oldClockOut, clockedInHours = 0,0,0,0,0
							noonFlag = "am"
						else:
							noonFlag = "pm"
							clockedInHours += interval

				oldClockOut = clockOut
				clockReadings = parseInput(next(csv_reader, None))

		hours = int(clockedInHours)
		mins = round((clockedInHours % 1) * 60)
		print(f"Total hours worked: {clockedInHours}, or {hours}hrs {mins}mins")

	except FileNotFoundError:
		print(f"File not found: {file_path}")
	except Exception as e:
		print(f"An error occurred: {e}")
