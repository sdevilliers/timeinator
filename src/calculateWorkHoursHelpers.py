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
	if not inputLine:
		return None, None

	return [
		[int(inputLine[1]), # clock in hr
		int(inputLine[2])], # clock in mins
		[int(inputLine[4]), # clock out hr
		int(inputLine[5])] # clock out mins
	], inputLine[0]

def getTimeStamp(hourOffset, clockReading):
	"""Ensures that the value returned is greater than prevTimeStamp by adding 12hrs if it is not"""
	hrsSinceMidnight = clockReading[0] + clockReading[1]/60
	return hrsSinceMidnight + hourOffset

def getData(hourOffsets, clockReadings):
	"""Returns the clockIn and clockOut hours since midnight and the interval between the two in hours"""
	clockIn = getTimeStamp(hourOffsets[0], clockReadings[0])
	clockOut = getTimeStamp(hourOffsets[1], clockReadings[1])

	return (clockIn, clockOut, clockOut - clockIn)

def dateChanged(previousDate, parsedDate):
	if not parsedDate:
		return False
	return previousDate != parsedDate

def getCorrectOffsets(previousOffsets, previousClockOut, previousDate, clockReadings, parsedDate):
	"""
	Returns the correct offsets for the given clock readings

	Parameters:
		previousOffsets (tuple): the previous offsets used to calculate the
		previous clock readings. Note that the previous clock readings should be
		for the same day as the current clock readings.
	"""

	correctOffsets = AM.offsets if dateChanged(previousDate, parsedDate) else previousOffsets
	clockIn, clockOut, _ = getData(correctOffsets, clockReadings)

	def offsetWorks():
		return previousClockOut <= clockIn and clockIn <= clockOut

	while not offsetWorks():
		correctOffsets = Offsets(correctOffsets).increment()
		if correctOffsets == None:
			raise ValueError(f"Invalid timestamps on {parsedDate}: {clockReadings[0]}:{clockReadings[1]} -> {clockReadings[2]}:{clockReadings[3]}. Clock ins more than 24h after midnight should be reported on the following day")
		clockIn, clockOut, _ = getData(correctOffsets, clockReadings)

	return correctOffsets

def describeInterval(hours):
	mins = round((hours % 1) * 60)
	return f"{hours:.2f}h or {hours:d}h {mins}min"

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

	clockedInHours = {}
	hoursDataPerDay = {}
	hourOffsets = AM.offsets # Allows us to track am (+0hr) vs pm (+12hr)

	try:
		with open(file_path, newline='') as csvfile:
			csv_reader = csv.reader(csvfile)
			next(csv_reader, None) # skip header

			while clockReadings:
				clockReadings, parsedDate = parseInput(next(csv_reader, None))
				hourOffsets = getCorrectOffsets(hourOffsets, oldClockOut, oldDate, clockReadings, parsedDate)

				clockIn, clockOut, interval = getData(hourOffsets, clockReadings)

				if hourOffsets == MIDNIGHT.offsets:
					print(f"Hey there buddy, you're working really late! Looks like you worked from {clockReadings[0]}:{clockReadings[1]}pm on {parsedDate} until {clockReadings[2]}:{clockReadings[3]}am the next day.")

				clockedInHours[parsedDate] = clockedInHours.get(parsedDate, 0) + interval
				hoursDataPerDay[parsedDate] = hoursDataPerDay.get(parsedDate, []).append((clockIn, clockOut))
				oldClockOut = clockOut
				oldDate = parsedDate

		print(f"Total hours worked: {describeInterval(clockedInHours)}")

	except FileNotFoundError:
		print(f"File not found: {file_path}")
	except Exception as e:
		print(f"An error occurred: {e}")
