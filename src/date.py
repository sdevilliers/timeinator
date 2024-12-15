import datetime

class Date:
	def __init__(self, date):
		"""yyyy-mm-dd"""
		self.isoDate = date
		self.year, self.month, self.day = map(int, date.split('-'))
		self.dateTime = datetime.date(self.year, self.month, self.day)
		self.week = self.dateTime.isocalendar()[1]
		self.weekday = self.dateTime.weekday()
		self.monthStr = self.dateTime.strftime('%B')
		self.dayOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][self.weekday]
		self.weekKey = 'week' + str(self.week)

	def __eq__(self, other):
		if isinstance(other, Date):
			return self.isoDate == other.isoDate
		return False