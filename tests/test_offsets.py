from src.offsets import Offsets

def test_init_with_key():
	assert Offsets("am").offsets == (0, 0)
	assert Offsets("am").key == "am"
	assert Offsets("noon").offsets == (0, 12)
	assert Offsets("noon").key == "noon"
	assert Offsets("pm").offsets == (12, 12)
	assert Offsets("pm").key == "pm"
	assert Offsets("midnight").offsets == (12, 24)
	assert Offsets("midnight").key == "midnight"

def test_init_with_offset():
	assert Offsets((0, 0)).offsets == (0, 0)
	assert Offsets((0, 0)).key == "am"
	assert Offsets((0, 12)).offsets == (0, 12)
	assert Offsets((0, 12)).key == "noon"
	assert Offsets((12, 12)).offsets == (12, 12)
	assert Offsets((12, 12)).key == "pm"
	assert Offsets((12, 24)).offsets == (12, 24)
	assert Offsets((12, 24)).key == "midnight"

def test_init_with_invalid_key():
	assert Offsets("invalid").offsets == "invalid"
	assert Offsets("invalid").key == "invalid"

def test_indexing():
	assert Offsets("am").offsets[0] == 0
	assert Offsets("midnight").offsets[1] == 24