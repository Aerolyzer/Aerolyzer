class horizon:
	
	def __init__(self):
		self.message = "Hello World"
	

	def _hello(self,i):
		x=0
		while x<i:
			print self.message
			x = x + 1
		return 0
