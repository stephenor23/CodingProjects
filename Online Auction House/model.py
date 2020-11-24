from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

# Each row corresponds to a user account, admin==True will grant the privelege to view all User' info
class User(db.Model):
	__tablename__ = "User"
	user_id = db.Column(db.Integer, primary_key=True)  # username could be PK but will face scaling issue
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), nullable=True)
	password = db.Column(db.String(30), nullable=False)
	is_admin = db.Column(db.Boolean, nullable=False)
	balance = db.Column(db.Float, nullable = False)
	available_balance = db.Column(db.Float, nullable=False)
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
		self.is_admin = False
		self.balance = 1000
		self.available_balance = self.balance


class Item(db.Model):
	__tablename__ = "Item"
	item_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False)
	description = db.Column(db.String(100), nullable=True)
	owner_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	def __init__(self, name, description="no description given", owner_id):
		self.name = name
		self.description = description
		self.owner_id = owner_id

# Each row of this table contains all of the data relating to 
# Data will not be deleted from this table when auctions close (maybe after a long time)
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
