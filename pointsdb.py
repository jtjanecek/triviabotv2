import sys
import sqlite3
from sqlite3 import Error
from datetime import datetime
from datetime import timedelta
import time
import logging
import os

class PointsDB():
	def __init__(self, mode='rwc'):
		this_file_dir = os.path.dirname(os.path.abspath(__file__))
		db_file = os.path.join(this_file_dir, 'points.db')
		db_file = "file:" + db_file + "?mode=" + mode
		logging.info("Using DB: {}".format(db_file))

		# This will raise an error if it can't connect
		self.conn = sqlite3.connect(db_file, uri=True, check_same_thread=False)

		self._cols = ['user', 'points']
		sql_create_min_table = """CREATE TABLE IF NOT EXISTS points (
									user text PRIMARY KEY,
									points integer NULL
									);
								"""

		c = self.conn.cursor()
		if mode != 'ro':
			c.execute(sql_create_min_table)

		sql = "CREATE UNIQUE INDEX IF NOT EXISTS sym_dt_idx ON points (user, points);"
		c.execute(sql)

		self.conn.commit()
		c.close()

	def get(self, user):
		user = user.lower().strip()
		c = self.conn.cursor()
		select = """SELECT points
					FROM points
					WHERE user = ?;
				"""
		vals = c.execute(select, [user]).fetchone()
		c.close()
		# Check if it exists first
		logging.info("Vals: {}".format(vals))
		if not vals:
			return 0
		return vals[0]

	def update(self, user, points):
		user = user.lower().strip()
		cur_points = self.get(user)
		c = self.conn.cursor()
		if cur_points == 0:
			select = """INSERT INTO points
						(points, user)
						values(?,?);
					"""
		else:
			select = """UPDATE points
						SET points = ?
						WHERE user = ?;
					"""
		c.execute(select, (points, user))
		self.conn.commit()
		c.close()