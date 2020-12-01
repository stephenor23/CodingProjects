class Round:

	def __init__(self, round_number):
		self.round_number = round_number
		self.carry = 0
		self.throw_one = 0
		self.throw_two = 0
		self.strike = False
		self.spare = False
		self.score = 0
		self.is_over = False

	def __repr__(self):
		if not self.strike:
			return "\n__Round {}__\nThrow One: {}\nThrow Two: {}\nScore: {}\n".format(self.round_number, self.throw_one, self.throw_two, self.score)
		else:
			return "\n__Round {}__\nThrow One: Strike!\nScore: {}\n".format(self.round_number, self.score)

	def reset_values(self):
		self.throw_one = 0
		self.throw_two = 0
		self.strike = False
		self.spare = False

	def is_valid_throw_one(self, throw_one):
		if throw_one in range(11):
			return True
		return False

	def is_valid_throw_two(self, throw_two):
		if throw_two < 0:
			return False
		elif throw_two + self.throw_one > 10:
			return False
		elif throw_two > 10:
			return False
		elif throw_two + self.throw_one == 10:
			self.spare = True
			return True
		else:
			return True

	def process_score(self):
		if self.carry == 0:
			self.score = self.throw_one + self.throw_two
		elif self.carry == 1:
			self.score = self.throw_one*2 + self.throw_two
		elif self.carry == 2:
			self.score = (self.throw_one + self.throw_two) * 2
		else:
			self.score = self.throw_one*3 + self.throw_two*2


	def play_round(self):
		print("___Round #{}".format(self.round_number+1))
		throw_one = int(input("Enter score of first throw >> "))
		if self.is_valid_throw_one(throw_one):
			self.throw_one = throw_one
			if throw_one != 10:  # wasn't a strike, go to second throw
				throw_two = int(input("Enter score of second throw >> "))
				if self.is_valid_throw_two(throw_two):
					self.throw_two = throw_two
				else:
					self.reset_values()
					self.play_round()
			else:
				print("Strike!")
				self.strike = True
		else:
			self.reset_values()
			self.play_round()
		self.process_score()

