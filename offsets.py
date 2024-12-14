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