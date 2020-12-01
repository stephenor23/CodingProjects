from round import Round
from tkinter import *
class Player:

	def __init__(self, player_name, root):
		self.player_name = player_name
		self.score = 0
		self.rounds = [Round(i) for i in range(10)]
		self.player_frame = Frame(root, borderwidth=3, relief="raised")
		self.name = Label(self.player_frame, borderwidth=5, relief="sunken", text=self.player_name)
		self.score_frames = [Frame(self.player_frame, borderwidth=3, relief="raised") for i in range(10)]
		self.top_subframes = [Frame(self.score_frames[i], borderwidth=3, relief="raised") for i in range(10)]
		self.bottom_subframes = [Frame(self.score_frames[i], borderwidth=3, relief="raised") for i in range(10)]
		self.throws = [[Label(self.top_subframes[i], text=self.rounds[i].throw_one), Label(self.top_subframes[i], text=self.rounds[i].throw_two)] for i in range(10)]
		self.scores = [Label(self.bottom_subframes[i], text=self.rounds[i].score) for i in range(10)]
		self.total_score_frame = Label(self.player_frame, borderwidth=3, relief="raised", text=self.score)
		self.display()


	def display(self):
		self.player_frame.pack(side=TOP)
		self.name.pack(side=LEFT)
		for i in range(10):
			self.score_frames[i].pack(side=LEFT)
			self.top_subframes[i].pack()
			self.bottom_subframes[i].pack()
			self.throws[i][0].pack(side=LEFT)
			self.throws[i][1].pack(side=RIGHT)
			self.scores[i].pack()
			self.total_score_frame.pack(side=RIGHT)

	def update_frames(self, i):
		self.throws[i][0].configure(text=self.rounds[i].throw_one)
		self.throws[i][1].configure(text=self.rounds[i].throw_two)
		self.scores[i].configure(text=self.rounds[i].score)
		self.total_score_frame.configure(text=self.score)


	def update_score(self, round_number):
		self.score += self.rounds[round_number].score

	def get_previous_round(self):
		for i in range(len(self.rounds)):
			if not self.rounds[i].is_over:  # the first round we find that isn't over will be the current one
				return self.rounds[i-1]

	def get_second_previous_round(self):
		for i in range(len(self.rounds)):
			if not self.rounds[i].is_over:  # the first round we find that isn't over will be the current one
				return self.rounds[i-2] 

	
	def get_next_carry(self):
		if self.rounds[1].is_over:  # when two or more rounds have been played
			previous_round = self.get_previous_round()
			if previous_round.spare:  # if the previous round resulted in a spare
				return 1
			else:
				if previous_round.strike:  # if the previous round was a strike
					if self.get_second_previous_round().strike:  # and if the round before that was a strike
						# if the last two throws were strikes
						return 3
					else:
						# if the last round was a strike but the one before wasn't
						return 2
				else:
					# if the last round wasn't a strike or spare
					return 0
		elif self.rounds[0].is_over:  # if we're on the second round
			previous_round = self.get_previous_round()
			if previous_round.strike:
				return 2
			elif previous_round.spare:
				return 1
			else:
				return 0
		else:  # we're on the very first round, impossible to have a previous strike/spare increase our score
			return 0

"""
def main():
	ste = Player("Stephen")
	for i in range(len(ste.rounds)):
		ste.rounds[i].carry = ste.get_next_carry()
		ste.rounds[i].play_round()
		ste.rounds[i].is_over = True
		ste.update_score(i)  # update player's total with their score for round i
		print(ste.rounds[i])

main()
"""
