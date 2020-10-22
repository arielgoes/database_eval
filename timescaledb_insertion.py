import psycopg2 as pg2
from psycopg2 import sql
import datetime
import random
import time
from threading import Thread
from subprocess import check_output

import sys
import os
import argparse
import logging
import subprocess
import shlex

DEFAULT_PROBES = 0
DEFAULT_DEVICES = 0

class DataBase():
	def __init__ (self, p=DEFAULT_PROBES, d=DEFAULT_DEVICES):
		#connect to the db
		self.conn = pg2.connect(
			host = "localhost",
			database = "probemon",
			user = "postgres",
			password = "123")    

		#cursor
		cur = self.conn.cursor()

		#drop and recreate table
		query = sql.SQL("drop table telemetry_data")
		cur.execute(query)
		query = sql.SQL("create table if not exists telemetry_data (timestamptz TIMESTAMPTZ, device INTEGER not null, queue_time INTEGER not null, process_time INTEGER not null)")
		cur.execute(query)

		#create hypertable
		cur.execute("SELECT create_hypertable('telemetry_data', 'timestamptz');")
		self.conn.commit()
		cur.close()


	# serie temporal - tempo de fila
	def insertion(self, probes, devices):
		cur = self.conn.cursor()

		#table's name
		table_name = "telemetry_data"
		
		data = []
		for self.p in range(probes):
			for self.d in range(devices):
				timestamptz = datetime.datetime.now()
				queue_time = random.randrange(1, 100)
				process_time = random.randrange(1, 200)
				row = [timestamptz, self.d, queue_time, process_time]
				data.append(row)
		args_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", x).decode("utf-8") for x in data)
		start = time.time() * 1000
		cur.execute("INSERT INTO telemetry_data VALUES " + args_str)
		end = time.time() * 1000 
		self.conn.commit()
		cur.close()
		#print("Insertion: " + str(end - start) + "ms")
		return (end - start) #time in ms


	#counts how many insertions were succesfull
	def count_insertion(self):
		cur =  self.conn.cursor()
		cur.execute("SELECT COUNT(*) FROM \"telemetry_data\";")
		total_count = list(cur.fetchone())
		total_count = total_count[0]
		self.conn.commit()
		cur.close()
		return total_count


	def getDevice(self):
		cur = self.conn.cursor()
		start = time.time() * 1000
		cur.execute("SELECT device FROM telemetry_data WHERE device = '1';")
		print(cur.fetchall())
		end = time.time() * 1000
		self.conn.commit()
		cur.close()
		return (end - start)
		
		return (end - start)

	def deletion(self):
		cur = self.conn.cursor()
		start = time.time() * 1000
		cur.execute("DELETE FROM telemetry_data;")
		end = time.time() * 1000
		self.conn.commit()
		cur.close()
		#print("Deletion: " + str(end - start) + "ms")
		return (end - start) #time in ms

	def close_conn(self):
		#close the connection
		self.conn.close()


def main():
	parser = argparse.ArgumentParser(description='TimescaleDB run manager')
	parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
	parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
	#parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

	args = parser.parse_args()
	
	#create connection to timescaledb
	db = DataBase(p=args.probes, d=args.devices)

	#insert
	time_insert = db.insertion(args.probes, args.devices)

	#query count
	total_count = db.count_insertion()

	#query get device
	time_get_device = db.getDevice()

	#delete all
	time_delete = db.deletion()

	#close connection
	db.close_conn()

	print("TimescaleDB" + ";" + str(args.probes) + ";" + str(args.devices) + ";" + str(total_count) + ";" +
		str(time_insert) + ";" + str(time_delete) + ";" + str(time_get_device) + ";" + "X")
	#PROBES;DEVICES;total_count;INSERTION_TIME;DELETION_TIME;GET_DEVICE;BATCH_SIZE(X) (TimescaleDB)


if __name__ == "__main__":
	sys.exit(main())
