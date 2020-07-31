import sqlite3
import os

class Database:

	db = None
	connection = None
	cursor = None


	def __init__(self, db_path):
		self.db = db_path


	def connect(self):
		self.connection = sqlite3.connect(self.db)
		self.cursor = self.connection.cursor()


	def analyze(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
		return self.cursor.fetchall()


	def execute(self, command):
		self.cursor.execute(command)
		self.connection.commit()


	def fetchAll(self):
		return self.cursor.fetchall()


	def remove(self):
		os.remove(self.db)


	def disconnect(self):
		self.connection.close()

