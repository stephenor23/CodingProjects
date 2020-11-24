import requests

BASE = "http://127.0.0.1:5000/"

def login():
	username = input("Enter username >> ")
	password = input("Enter your password >> ")
	return requests.get(BASE + f"user/{username}")

def signup():
	username = input("Enter your name >> ")
	email = input("Enter your email address >> ")
	password = input("Create a password >> ")
	return requests.put(BASE + f"user/{username}", {"username": username, "email": email, "password": password})

def delete(username):
	return requests.delete(BASE + f"user/{username}")


print(login().json())


# response = requests.put(BASE + "user", {"username": "Jake", "email": "jake@haemish.galway", "password": "jake"})


