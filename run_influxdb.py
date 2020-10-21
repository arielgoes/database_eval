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

	cmd = "python3.7 influxdb_insertion.py" \
	" --probes %d --devices %d --batchsize %d" % (args.probes, args.devices, args.batchsize)

	param = shlex.split(cmd)
	subprocess.call(param)


if __name__ == '__main__':
	sys.exit(main())