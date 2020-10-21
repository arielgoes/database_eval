#!/bin/bash

echo "Choose the DBMS to run experiments, then press [ENTER]"
echo "[1] InfluxDB -- [2] TimescaleDB -- [3] PostgreSQL"
read RUN


echo "Available parameters: -p [Number of Probes], -d [Number of Devices] -b [Batch Size (InfluxDB)]"
read -p "Enter values in respective order (-p -d -b):" PROBES DEVICES BATCH_SIZE

case $RUN in
	1) 
		echo "[1] InfluxDB (case)"
		#python3.7 influxdb_insertion.py -p $PROBES -d $DEVICES -b $BATCH_SIZE
	;;
	2)
		echo "[2] TimescaleDB (case)"
		#python3.7 timescaledb_insertion.py -p $PROBES -d $DEVICES
	;;
	3)
		echo "[3] PostgreSQL (case)"
	;;
	*)
		echo "ERROR: Invalid option! (case)"
	;;
esac

#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;BATCH_SIZE (InfluxDB)
#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;X (TimescaleDB)