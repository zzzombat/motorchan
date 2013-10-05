
from pymongo import MongoClient
from tornado.options import options
from application import Application

def main():
	
	client = MongoClient(options.dburl)
	db = client.motorchan
	adminuser = db.users.find_one({"username":"admin"})
	if adminuser is None:
		db.users.insert({'username': 'admin', 'password': '1234'})
