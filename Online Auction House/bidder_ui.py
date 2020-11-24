def log_in():
	username = input("Enter your username: ") 
	password = input("Enter your password: ")
def view_auction():
	auction_id = int(input("Enter ID of Auction you'd like to view: "))
	display_auction(auction_id)


def log_out():
	pass
def display_auction():
	pass

def main():
	options = {"Log In": log_in,
			   "View Auction": view_auction,
			   "My Items": view_items
			   }

main()
