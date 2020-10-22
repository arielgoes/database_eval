from influxdb import InfluxDBClient
import random
import time
from datetime import datetime

import sys
import os
import argparse
import logging
import subprocess

DEFAULT_BATCH_SIZE = 5000

client = InfluxDBClient(host='localhost', port=8086)

#overwrites old database
client.drop_database("ProbeMon")
client.create_database("ProbeMon")

#use recreated database
client.switch_database("ProbeMon")

#p = # probes; d = # devices; b = batch_size
def insertion(p, d, b):
	data = []
	for i in range(p): #number of probes
		for j in range(d): #number of devices
			#q_time = random.randint(1, 15) #time in ms
			#p_time = random.randint(5, 200) #time in ms
			di_data =   {"measurement": "telemetry_data", 
						"tags": {"id" : j},
						"time": int(time.time_ns()) - random.randint(1,9999),
						"fields": {"queue_time": random.randint(1, 10), "process_time": random.randint(1,10)}}
			data.append(di_data)
			
	start = int(round(time.time()) * 1000)
	if(b > p*d):
		print("WARNING: 'batch_size' is too huge, Maximum value is (p * d) = %d, using %d", (i*j), DEFAULT_BATCH_SIZE)
		b = DEFAULT_BATCH_SIZE
	elif(b <= 0):
		print("WARNING: 'batch_size' is too small. Mininum value is 1, using %d", DEFAULT_BATCH_SIZE)
		b = DEFAULT_BATCH_SIZE
	client.write_points(data, batch_size=b)
	end = int(round(time.time()) * 1000)
	#print("Insertion time: " + str(end - start) + "ms") #time in 'ms' precision
	return (end - start)


def deletion(d):
	start = int(round(time.time()) * 1000)
	client.delete_series(database='ProbeMon', measurement='telemetry_data')
	end = int(round(time.time()) * 1000)
	#print("Deletion time: " + str(end - start) + "ms") #time in 'ms' precision
	return (end - start)


def main():
	parser = argparse.ArgumentParser(description='InfluxDB insertion script')
	parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
	parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
	parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

	args = parser.parse_args()

	#query insert
	time_insert = insertion(p=args.probes, d=args.devices, b=args.batchsize)

	#query select count total insertions
	total_count = client.query('SELECT COUNT("process_time") FROM "telemetry_data";')#.items();
	total_count = list(total_count.get_points(measurement='telemetry_data'))
	total_count = total_count[0]['count']

	time_delete = deletion(d=args.devices)

	print("InfluxDB" + ";" + str(args.probes) + ";" + str(args.devices) + ";" + str(total_count) + ";" +
		str(time_insert) + ";" + str(time_delete) + ";" + str(args.batchsize))
	#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;BATCH_SIZE (InfluxDB)

if __name__ == '__main__':
	sys.exit(main())