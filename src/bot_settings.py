import os

"""
Application Settings
"""

USERNAME = 'c5bot'
PASSWORD = os.environ['REDDIT_PASSWORD']
SUBREDDIT = 'concrete5'

DATABASE = {
	'host' : 'localhost', 
	'user' : os.environ['DATABASE_USER'],
	'password' : os.environ['DATABASE_PASSWORD'],
	'dbname' : os.environ['DATABASE_NAME']
}