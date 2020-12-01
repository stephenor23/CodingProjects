from round import Round
from player import Player
from tkinter import *

def show_winner(players):

	print("__Final Scores__")
	for player in players:
		print(f"{player.player_name}: {player.score}")
	
	print()

	highest_score = 0
	winners = []
	for player in players:
		if player.score > highest_score:
			winners = [player.player_name]
			highest_score = player.score
		elif player.score == highest_score:  # tied highest score
			winners.append(player.player_name)
	if len(winners) == 0:
		print("There are no winners")  # this should never happen
	elif len(winners) == 1:
		print(f"The winner is {winners[0]} with a score of {highest_score}.")
	else:
		s = ""
		for winner in winners:
			s += "{}, ".format(winner)
		print(f"{s}are the winners with a score of {highest_score}")


def main():
	root = Tk()

	players = [Player("Player 1", root), Player("Player 2", root)]

	for player in players:
		player.display()
	
	for i in range(10):
		print(i)
		for player in players:
			print("{}'s turn".format(player.player_name))
			player.rounds[i].carry = player.get_next_carry()
			player.rounds[i].play_round()
			player.rounds[i].is_over = True
			player.update_score(i)
			player.update_frames(i)
			print(player.rounds[i])
	
	show_winner(players)

	root.mainloop()


main()
