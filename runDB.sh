#!/bin/bash

echo "Choose the DBMS to run experiments, then press [ENTER]"
echo "[1] InfluxDB -- [2] TimescaleDB -- [3] PostgreSQL"
read RUN

echo "How many times you want to run it? NOTE: N > 0"
read N

if [[ $N -le 0 ]]; then
	echo "Invalid 'N'"
	exit 1
fi

echo "Available parameters: -p [Number of Probes], -d [Number of Devices] -b [Batch Size (InfluxDB)]"
read -p "Enter values in respective order (-p -d -b):" PROBES DEVICES BATCH_SIZE

case $RUN in
	1)
		for((i=0;i<N;i++)); do
			echo "[1] InfluxDB (case)"
			python3.7 run_influxdb.py -p $PROBES -d $DEVICES -b $BATCH_SIZE
		done
	;;
	2)
		for((i=0;i<N;i++)); do
			echo "[2] TimescaleDB (case)"
			python3.7 run_timescaledb.py -p $PROBES -d $DEVICES
		done
	;;
	3)
		for((i=0;i<N;i++)); do
			echo "[3] PostgreSQL (case)"
		done
	;;
	*)
		echo "ERROR: Invalid option! (case)"
	;;
esac

#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;BATCH_SIZE (InfluxDB)
#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;X (TimescaleDB)