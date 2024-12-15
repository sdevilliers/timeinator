class Offsets:
	def __init__(self, identifier):
		offsetsByKey = {
			"am": (0, 0),
			"noon": (0, 12),
			"pm": (12, 12),
			"midnight": (12, 24)
		}
		keysByOffset = {tuple(v): k for k, v in offsetsByKey.items()}

		self.offsets = offsetsByKey.get(identifier, identifier)
		self.key = keysByOffset.get(identifier, identifier)

	@classmethod
	def optional(cls, identifier):
		instance = cls(identifier)
		if instance.offsets == instance.key:
			return None
		return instance

	def increment(self):
		nextOffsetDict = {
			"am": "noon",
			"noon": "pm",
			"pm": "midnight",
		}
		nextOffset = nextOffsetDict.get(self.key, None)
		return Offsets(nextOffset).offsets if nextOffset else None

	def __eq__(self, other):
		if isinstance(other, Offsets):
			return self.offsets == other.offsets and self.key == other.key
		return False