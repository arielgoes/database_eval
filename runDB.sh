#!/bin/bash

echo "Choose the DBMS to run experiments, then press [ENTER]"
echo "[1] InfluxDB -- [2] TimescaleDB -- [3] PostgreSQL"
read RUN

if [[ $RUN -le 0 || $RUN -ge 4 ]]; then
	echo "ERROR: Invalid option! (case)"
	exit 1
fi

echo "How many times you want to run it? NOTE: N > 0"
read N

if [[ $N -le 0 ]]; then
	echo "N must be greater than 0"
	exit 1
fi

echo "Available parameters: -p [Number of Probes], -d [Number of Devices] -b [Batch Size (InfluxDB)]"
read -p "Enter values in respective order (-p -d -b):" PROBES DEVICES BATCHSIZE

if [[ $((PROBES*DEVICES)) -lt 1000 ]]; then
	echo "p * d must be >= 1000"
	exit 1
fi

case $RUN in
	1)
		echo "[1] InfluxDB (case)"
		for((i=0;i<N;i++)); do
			echo "Execution #" $i
			for((j=1000;j<=$((PROBES*DEVICES));j*=10)); do
				python3.7 run_influxdb.py -p $PROBES -d $DEVICES -b $BATCHSIZE
			done
		done
	;;
	2)
		echo "[2] TimescaleDB (case)"
		for((i=0;i<N;i++)); do
			for((j=1000;j<=$((PROBES*DEVICES));j*=10)); do
				python3.7 run_timescaledb.py -p $PROBES -d $DEVICES
			done
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