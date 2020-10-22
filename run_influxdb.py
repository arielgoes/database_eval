from influxdb import InfluxDBClient
import random
import time
from datetime import datetime

import sys
import os
import argparse
import logging
import subprocess
import shlex

DEFAULT_BATCH_SIZE = 5000

def main():
	parser = argparse.ArgumentParser(description='InfluxDB run manager')
	parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
	parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
	parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

	args = parser.parse_args()

	batch_size = args.batchsize

	if(batch_size > args.probes*args.devices):
		#print("WARNING: 'batch_size' is too huge, Maximum value is (p * d) = %d, using %d", (i*j), DEFAULT_BATCH_SIZE)
		batch_size = DEFAULT_BATCH_SIZE
	elif(batch_size <= 0):
		#print("WARNING: 'batch_size' is too small. Mininum value is 1, using %d", DEFAULT_BATCH_SIZE)
		batch_size = DEFAULT_BATCH_SIZE

	cmd = "python3.7 influxdb_insertion.py" \
	" --probes %d --devices %d --batchsize %d" % (args.probes, args.devices, batch_size)

	param = shlex.split(cmd)
	subprocess.call(param)


if __name__ == '__main__':
	sys.exit(main())