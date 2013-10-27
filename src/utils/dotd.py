import requests
from bs4 import BeautifulSoup
from datetime import date
import time
from bot_settings import SUBREDDIT
from logger import Logger


#all deal of the day parsers should inherit from this object and implement get()
class DealOfTheDay(object):

	def __init__(self, reddit, logger):
		self.reddit = reddit
		self.logger = logger

	def get(self):
		"""
		Return the current deal of the day as a string - Child classes need to implement this
		"""
		raise NotImplementedError

	def is_duplicate(self, post_title):
		"""Check if a link with the specified title has already been posted"""

		#search() returns a generator so len() doesn't work. If there are any results set duplicate to true and break
		matching_posts = self.reddit.search(query=post_title, subreddit=SUBREDDIT)
		duplicate = False
		for post in matching_posts:
			duplicate = True
			break
		return duplicate

	def post_to_reddit(self):
		ticks = str(int(time.time()))
		title = self.get()
		msg, msg_type = '', ''

		#add a random query string so the link isn't a duplicate
		link = self.DOTD_URL + "?d=" + ticks
		#reddit's maxlength for post titles is 300 - if we're over that truncate and add "..."
		if len(title) > 300:
			title = title[:297] + '...'

		#only post the dotd if the bot hasn't posted it yet
		if not self.is_duplicate(title):
			try:
				#self.reddit.submit(SUBREDDIT, title, url=link, raise_captcha_exception=True)
				msg = 'Post submitted. Title: %s - Link: %s' % (title, link)
				msg_type = Logger.MSG_TYPES['success']
			except praw.errors.InvalidCaptcha as e:
				msg = 'Post not submitted. Reason: InvalidCaptcha exception. Title: %s - Link: %s' % (title, link)
				msg_type = Logger.MSG_TYPES['error']
			except praw.errors.AlreadySubmitted as e:
				msg = 'Post not submitted. Reason: AlreadySubmitted exception. Title: %s - Link: %s' % (title, link)
				msg_type = Logger.MSG_TYPES['warning']
		else:
			msg = 'Post not submitted. Reason: is duplicate. Title: %s - Link: %s' % (title, link)
			msg_type = Logger.MSG_TYPES['info']

		self.logger.log(msg, msg_type)


class DealOfTheDayHtml(DealOfTheDay):
	"""
	Parses out the concrete5.org deal of the day from HTML.
	This is a last resort since the core team hasn't created any alternative feeds.
	If the HTML of the DOTD_URL changes at all this will break
	"""

	def __init__(self, reddit, logger):
		self.DOTD_URL = 'http://www.concrete5.org/marketplace/deal/'
		super(DealOfTheDayHtml, self).__init__(reddit, logger)

	def get(self):
		r = requests.get(self.DOTD_URL)
		html = r.text
		soup = BeautifulSoup(html)
		title = '[DotD] %s: ' % date.today().strftime('%m/%d/%Y')
		deal_str = self.get_deal_str(soup)
		price_str = self.get_price_str(soup)
		title += '%s - %s' % (deal_str, price_str)
		return title

	def get_deal_str(self, soup):
		"""
		Returns a string containing a comma-delimited list of addons in the DOTD
		"""
		deals = []
		deal_articles = soup.select(".addon-list article")
		deal_str = ''
		for deal in deal_articles:
			deals.append(deal.a.string)
		deal_str += ', '.join(deals)
		return deal_str

	def get_price_str(self, soup):
		"""
		Returns a string that shows the price of the DOTD
		"""
		price_str = ''
		h2s = soup.select('h2.green-sub')
		for h2 in h2s:
			if h2.string == 'Total':
				p = h2.find_next_sibling('p')
				price_str = p.string
		return price_str