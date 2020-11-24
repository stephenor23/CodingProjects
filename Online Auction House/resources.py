import main
from flask_restful import Resource, reqparse

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, help="unique username of user", required=True)
user_put_args.add_argument("email", type=str, help="email address of user")
user_put_args.add_argument("password", type=str, help="the user's passowrd")

class User(Resource):
	def get(self, user_id):
		user = main.User.query.filter_by(user_id=user_id).first()
		return { "user_id": user.user_id,
				 "username": user.username,
				 "email": user.email,
				 "password": user.password,
				 "is_admin": user.is_admin,
				 "balance": user.balance,
				 "available_balance": user.available_balance}
	def put(self):
		args = user_put_args.parse_args()
		main.db.session.add(User(args["name"], args["email"], args["password"]))
		main.db.session.commit()
		user = model.User.query.filter_by(username=username).first()
		return { "user_id": user.user_id,
				 "username": user.username,
				 "email": user.email,
				 "password": user.password,
				 "is_admin": user.is_admin,
				 "balance": user.balance,
				 "available_balance": user.available_balance}

class Item(Resource):
	def get(self, item_id):
		item = model.Item.query.filter_by(item_id=item_id).first()
		return {"item_id": item.item_id,
				"name": item.name,
				"description": item.description,
				"owner_id": item.owner_id}

# Each row of this table contains all of the data relating to 
# Data will not be deleted from this table when auctions close (maybe after a long time)
class Auction(Resource):
	def get(self, auction_id):
		auction = model.Auction.query.filter_by(auction_id=auction_id).first()
		return {"auction_id": auction.auction_id,
				"item_id": auction.item_id,
				"seller_id": auction.seller_id,
				"highest_bidder_id": auction.highest_bidder_id,
				"current_bid": auction.current_bid,
				"time_started": auction.time_started,
				"time_closed": auction.time_closed,
				"is_open": auction.is_open
				}

# User will be sent notifications based on activity in the auctions they're interested in.
# This table will store these notifications
class Notification(Resource):
	def get(self, notification_id):
		notification = model.Notification.query.filter_by(notification_id=notification_id).first()
		return {"notification_id": notification.notification_id,
				"user_id": notification.user_id,
				"auction_id": notification.auction_id,
				"information": notification.information,
				"time": notification.time
				}

