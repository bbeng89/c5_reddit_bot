"""
Author: Blake Bengtson (AKA bbeng89)


Run this script to start the /r/concrete5 reddit bot
"""
from utils.dotd import DealOfTheDay, DealOfTheDayHtml
from bot_settings import USERNAME, PASSWORD
import praw

def main():
	#create reddit object
	reddit = praw.Reddit(user_agent="c5_reddit_bot")
	reddit.login(USERNAME, PASSWORD)

	#post the deal of the day
	dotd = DealOfTheDayHtml(reddit)
	dotd.post_to_reddit()

if __name__ == '__main__':
	main()