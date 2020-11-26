from flask import Flask, request, render_template, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=10)  # sessions times out after 10 minutes
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bidderdb.sqlite3"  # uri for database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):  # contains details of each user
	__tablename__ = "User"
	user_id = db.Column(db.Integer, primary_key=True)  # username could be PK but will face scaling issue
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), nullable=True)
	password = db.Column(db.String(30), nullable=False)
	is_admin = db.Column(db.Boolean, nullable=False)
	balance = db.Column(db.Float, nullable = False)
	available_balance = db.Column(db.Float, nullable=False)  # user may not be able to bid money that is already "tied up" in other auctions
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.is_admin = False
		self.balance = 1000
		self.available_balance = self.balance


class Item(db.Model):  # record of every items on the system
	__tablename__ = "Item"
	item_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False)
	description = db.Column(db.String(100), nullable=True)
	owner_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	def __init__(self, name, description, owner_id):
		self.name = name
		self.description = description
		self.owner_id = owner_id

# Each row of this table contains all of the data relating to one auction
# Data will not be deleted from this table when auctions closes
class Auction(db.Model):
	__tablename__ = "Auction"
	auction_id = db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey("Item.item_id"), nullable=False)
	seller_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	highest_bidder_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=True)
	current_bid = db.Column(db.Float, nullable=False)
	time_started = db.Column(db.DateTime, nullable=False)
	time_closed = db.Column(db.DateTime, nullable=False)
	is_open = db.Column(db.Boolean, nullable=False)
	def __init__(self, item_id, seller_id, current_bid, days):
		self.item_id = item_id
		self.seller_id = seller_id
		self.current_bid = current_bid
		self.time_started = datetime.now()
		self.time_closed = self.time_started + timedelta(days)
		self.is_open = True

# User will be sent notifications based on activity in the auctions they're interested in.
# This table will store these notifications
class Notification(db.Model):
	__tablename__ = "notifications"
	notification_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))
	auction_id = db.Column(db.Integer, db.ForeignKey("Auction.auction_id"))
	information = db.Column(db.String(50), nullable=False)
	time = db.Column(db.DateTime, nullable=True)
	def __init__(self, user_id, auction_id, information):
		self.user_id = user_id
		self.auction_id = auction_id
		self.information = information
		self.time = datetime.now()



@app.route("/")
def root():
	return redirect(url_for("home"))

@app.route("/home")
def home():
	if "name" in session:  # if the user is logged in 
		return render_template("home.html")
	else:
		flash("You might want to log in.")  # prompt user to log in
		return render_template("home.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":  # if sign-in form filled in
		corresp_db_entry = User.query.filter_by(username=request.form["nm"]).first()  # reference to User obj in db
		if corresp_db_entry:  # if the user is found in the database
			if request.form["pw"] == corresp_db_entry.password:  # if the password entered is correct

				# create a session
				session.permanent = True
				session["name"] = corresp_db_entry.username
				session["id"] = corresp_db_entry.user_id
				session["admin"] = corresp_db_entry.is_admin

				flash("You have succesfully signed in.")
				return redirect(url_for("home"))
			else:  # if password is wrong
				flash("Incorrect password.")
				return redirect(url_for("login"))
		else:  # if we can't find the user
			flash("Could not find this username")
			return redirect(url_for("login"))
	else:  # about to sign in
		if "name" in session:
			flash("You're already logged in.")
			return redirect(url_for("home"))
		else:
			return render_template("login.html")

@app.route("/logout/")
def logout():
	if "name" in session:

		# close the session
		session.pop("name", None)
		session.pop("id", None)
		session.pop("admin", None)

		flash("You have now been signed out")
		return redirect(url_for("home"))
	else:  # if user isn't signed in
		flash("You're not signed in.")
		return redirect(url_for("login"))


@app.route("/signup/", methods=["GET", "POST"])
def signup():
	if "name" in session:
		# already signed in
		flash("You're already signed in")
		return redirect(url_for("home"))
	else:
		if request.method == "POST":  # if user has just submitted the form
			rf = request.form
			db.session.add(User(rf["nm"], rf["em"], rf["pw"]))  # create a new entry in our User table
			db.session.commit()

			# start a session with the new user's details
			session["name"] = rf["nm"]
			session["id"] = User.query.filter_by(username=session["name"]).first().user_id
			session["admin"] = User.query.filter_by(username=session["name"]).first().is_admin
			
			flash("You have succesfully signed up!")
			return redirect(url_for("home"))
		else:
			return render_template("signup.html")  # display sign-up form for user


@app.route("/registeritem/", methods=["GET", "POST"])
def registeritem():
	if "name" in session:  # check is user is logged in
		if request.method == "POST":
			rf = request.form
			db.session.add(Item(rf["nm"], rf["ds"], session["id"]))  # add submitted item details to Item table
			db.session.commit()
			flash("Item registered")
			return redirect(url_for("itemlist"))
		else:
			return render_template("registeritem.html") # display item register html page to user
	else:  # user isn't signed in
		flash("You need to sign in ")  
		return redirect(url_for("login"))


@app.route("/registerauction/", methods=["GET", "POST"])
def registerauction():
	if "name" in session:  # if user is signed in 
		if request.method == "POST":

			rf = request.form

			if session["id"] != Item.query.filter_by(item_id=rf["id"]).first().owner_id:  # prevent user from auctioning other people's items
				flash("You can't sell someone else's item")
				return redirect(url_for("home"))
			elif Auction.query.filter_by(item_id=rf["id"], is_open=True).count():  # prevent the same item from being auctioned off twice
				flash("The same item can't be auctioned twice")
				return redirect(url_for("registerauction", method="GET"))
			db.session.add(Auction(rf["id"], session["id"], rf["sp"], int(rf["du"])))  # add new auction to Auction table
			db.session.commit()
			flash("Auction registered")
			return redirect(url_for("auctionlist"))

		else:
			return render_template("registerauction.html")
	else:
		flash("You need to sign in ")
		return redirect(url_for("login"))


@app.route("/adminregister/", methods=["GET", "POST"])
def adminregister():
	if "name" in session:
		if not session["admin"]:
			if request.method == "POST":

				# entry of "secret" word allows user to become an admin 
				if request.form["sw"].lower() in ["yes", "baile átha cliath", "baile atha cliath"]:
					User.query.filter_by(user_id=session["id"]).first().is_admin = True  # update User entry 
					db.session.commit()
					session["admin"] = True  # update session
					flash("With great power comes great responsibility...")
					return redirect(url_for("home"))
				else:
					flash("Incorrect secret word")
					return redirect(url_for("home"))
			else:
				return render_template("adminregister.html")
		else:
			flash("You're already an admin")
			return redirect(url_for("home"))
	else:
		flash("please log in")
		return redirect(url_for("login"))

# allows user to add money to their account (for free)
@app.route("/addcredit", methods=["GET", "POST"])
def addcredit():
	if "name" in session:  # if logged in 
		if request.method == "POST":
			amount = float(request.form["am"])
			if amount > 0:  # user must enter non-negative amount
				User.query.filter_by(user_id=session["id"]).first().balance += amount  # update User entry
				User.query.filter_by(user_id=session["id"]).first().available_balance += amount
				db.session.commit()
				return redirect(url_for("home"))
			else:
				flash("enter a non-negative amount")
				return redirect(url_for("addcredit"))
		else:
			return render_template("addcredit.html")
	else:
		flash("Please log in")
		return redirect(url_for("login"))


@app.route("/notifications")
def notifications():
	if "name" in session:
		notifications = Notification.query.filter_by(user_id=session["id"]).all()
		return render_template("notifications.html", notifications=notifications, date_format="%d/%m/%Y", time_format="%H:%M")
	else:
		flash("Please sign in")
		return redirect(url_for("login"))



@app.route("/userlist/")
def userlist():
	if "name" in session:
		return render_template("userlist.html", table_data=User.query.all())
	else:
		flash("You need to sign in.")
		return redirect(url_for("login"))


@app.route("/itemlist/")
def itemlist():
	if session["admin"]:  # only admins are allowed to view the entire item registry
		return render_template("itemlist.html", table_data=Item.query.all(), foreign_table_reference=User)
	else:
		flash("Page only accessible to admins")
		return redirect(url_for("home"))


@app.route("/viewmyitems/")
def viewmyitems():
	if "name" in session:  # any user can view their own item registry
		return render_template("viewmyitems.html", username=session["name"], table_data=Item.query.filter_by(owner_id=session["id"]).all())
	else:
		flash("You need to log in first.")
		return redirect(url_for("login"))


# allows the user to make a bid on another user's auction
@app.route("/make_bid/<id>", methods=["GET", "POST"])
def make_bid(id):
	if request.method == "GET":
		return render_template("make_bid.html", user_table=User, item_table=Item, auction_table=Auction, id=id)
	else:
		bid = float(request.form["bid"])  # the amount the buyer wishes to bid
		auction_obj = Auction.query.filter_by(auction_id=id).first()
		if bid <= auction_obj.current_bid:  # can't bid less than current bid
			flash("Invalid bid amount")
			return redirect(f"/make_bid/{id}")
		elif User.query.filter_by(user_id=session["id"]).first().available_balance < bid:  # check bidder has enough money
			flash("You don't have enough money to bid this much")
			return redirect(f"/make_bid/{id}")
		elif session["id"] == auction_obj.seller_id:  # check user isn't bidding on their own auction
			flash("You can't bid on your own auction")
			return redirect(f"/make_bid/{id}")
		elif auction_obj.time_closed < datetime.now():  # check if the auction is still open
			flash("this auction is closed")
			return redirect(f"/make_bid/{id}")

		auction = Auction.query.filter_by(auction_id=id).first()  # this is the Auction table entry of the auction in question
		
		# return to the previous bidder's available_balance the amount that they bid on this auction, as they have been outbid
		last_highest_bidder = User.query.filter_by(user_id=auction.highest_bidder_id).first()
		if last_highest_bidder != None:  # if this isn't the first bid (ie. there is another user who has now been outbid)
			last_highest_bidder.available_balance += auction.current_bid  # "un-tie" the last highest bidders funds from this auction
			notify(last_highest_bidder.user_id, id, "You have been outbid in this auction.")  # send them a notification letting them know they've been outbid

		# to avoid defecit spending, we use available_balance to keep track of how much of their money a bidder has the right to bid/spend
		User.query.filter_by(user_id=session["id"]).first().available_balance -= bid
		auction.current_bid = bid
		auction.highest_bidder_id = session["id"]  # update Auction table with info of new highest bidder
		auction.time_closed += timedelta(minutes=1)  # increment time so someone can re-bid, deter "ninjas"

		db.session.commit()

		notify(auction.seller_id, id, "{} has bid {} on this auction.".format(session["name"], bid))
		flash("Bid successful.")
		return redirect(url_for("auctionlist"))

# list of all auctions and relevant information
@app.route("/auctionlist/")
def auctionlist():
	update_auctions()
	if "name" in session:
		join1 = db.session.query(Auction, User).outerjoin(User, Auction.seller_id == User.user_id).order_by(Auction.auction_id.asc()).all()
		join2 = db.session.query(Auction, Item).outerjoin(Item, Auction.item_id == Item.item_id).order_by(Auction.auction_id.asc()).all()
		return render_template("auctionlist.html", auction_user_join=join1, auction_item_join=join2, user_table=User, dt_format="%d/%m/%Y @ %H:%M")
	flash("You need to sign in")
	return redirect(url_for("login"))

def close_auction(id):  # an auction is closed only when its time limit has run out

	auction = Auction.query.filter_by(auction_id=id).first()  # find Auction entry bid id
	winner_id = auction.highest_bidder_id  # the highest bidder is now the winner
	auctioneer_id = auction.seller_id

	auction.is_open = False  # close the auction
	User.query.filter_by(user_id=auction.seller_id).first().balance += auction.current_bid  # give money to auctioneer
	User.query.filter_by(user_id=auction.seller_id).first().available_balance += auction.current_bid 
	Item.query.filter_by(item_id=auction.item_id).first().owner_id = auction.highest_bidder_id  # give item to highest bidder
	User.query.filter_by(user_id=winner_id).first().balance -= auction.current_bid  # take the money from the user
	db.session.commit()

	notify(winner_id, id, "You have won this auction")
	notify(auctioneer_id, id, "Your auction has been closed")


def notify(user_id, auction_id, message):
	db.session.add(Notification(user_id, auction_id, message))
	db.session.commit()


def update_auctions():
	for auction in Auction.query.order_by(Auction.auction_id.asc()).all():
		if auction.time_closed < datetime.now():
			close_auction(auction.auction_id)

if __name__ == "__main__":
	db.create_all()
	update_auctions()
	app.run(debug=True)
