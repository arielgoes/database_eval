import psycopg2 as pg2
from psycopg2 import sql
import datetime
import random
import pytz
import time
from threading import Thread
from subprocess import check_output

import sys
import os
import argparse
import logging
import subprocess
import shlex


def main():
	parser = argparse.ArgumentParser(description='TimescaleDB run manager')
	parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
	parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
	#parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

	parser = argparse.ArgumentParser(description='TimescaleDB run manager')
	parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
	parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
	#parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

	args = parser.parse_args()

	cmd = "python3.7 timescaledb_insertion.py" \
	" --probes %d --devices %d" % (args.probes, args.devices)
	#" --probes %d --devices %d --batchsize %d" % (args.probes, args.devices, args.batchsize)

	param = shlex.split(cmd)
	subprocess.call(param)


if __name__ == '__main__':
	sys.exit(main())