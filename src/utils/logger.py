import MySQLdb as db
from datetime import datetime
from bot_settings import DATABASE

class Logger(object):
	"""Base class for loggers"""

	MSG_TYPES = {
		'error': 'Error',
		'warning': 'Warning',
		'info': 'Info',
		'success': 'Success'
	}

	def log(self, message, msg_type):
		raise NotImplementedError


class StdOutLogger(Logger):

	def log(self, message, msg_type):
		print "[%s] %s - %s" % (msg_type, datetime.now(), message)


class MySQLLogger(Logger):

	TABLE = 'botlog'

	def log(self, message, msg_type):
		q = 'INSERT INTO ' + MySQLLogger.TABLE + ' (log_time, msg_type, message) VALUES (%s, %s, %s)'
		args = [datetime.now(), msg_type, message]
		self.execute(q, args)

	def execute(self, query, args):
		try:
			con = db.connect(DATABASE['host'], DATABASE['user'], DATABASE['password'], DATABASE['dbname'])
			con.set_character_set('utf8')
			cur = con.cursor()
			cur.execute(query, args)
			con.commit()
			cur.close()
			con.close()
		except db.Error, e:
			print 'SQL Error: %s %s' % (e.args[0], e.args[1])