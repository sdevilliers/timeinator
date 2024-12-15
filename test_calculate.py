import pytest
from calculateWorkHoursHelpers import calculate

def test_calculate_single_day():
	printInputs = []
	print = lambda x: printInputs.append(x)
	def input(prompt):
		switch = {
			"Enter the path to your CSV file: ": "../test-data/single-day.csv"
		}
		return switch.get(prompt, "")

	calculate(print, input)
	expected = ["2024", "August", "Mon 26: 8.92h or 8h 55min", "Mon 26 -> Mon 26: 8.92h or 8h 55min"]
	assert printInputs[-len(expected):-1] == expected

def test_calculate_multiple_days():
	printInputs = []
	print = lambda x: printInputs.append(x)
	def input(prompt):
		switch = {
			"Enter the path to your CSV file: ": "../test-data/multi-day.csv"
		}
		return switch.get(prompt, "")

	calculate(print, input)
	expected = ["2024","August", "Mon 26: 8.92h or 8h 55min", "Tue 27: 9.02h or 9h 1min", "Wed 28: 7.80h or 7h 48min", "Thu 29: 7.60h or 7h 36min", "Mon 26 -> Thu 29: 33.33h or 33h 20min", "September", "Tue  3: 4.69h or 4h 41min", "Tue  3 -> Tue  3: 4.69h or 4h 41min"]
	assert printInputs[-len(expected):-1] == expected