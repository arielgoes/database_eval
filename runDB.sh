#!/bin/bash

#echo "Insertions = <probes> * 200"
#echo "Usage: <repetitions> <batch_size> <probes>"
read N BATCH_SIZE PROBES 

if [[ $N -le 0 || $PROBES -le 0 ]]; then
	echo "Usage: <N> and <probes> must be greater than 0"
	exit 1
fi

for((j=5;j<=$PROBES;j*=10)); do
	for((i=0;i<$N;i++)); do
		#echo "Execution #" $i
		python3.7 run_timescaledb.py -p $j >> out.txt
	done
done

for((j=5;j<=$PROBES;j*=10)); do
	for((i=0;i<$N;i++)); do
		#echo "Execution #" $i
		python3.7 run_influxdb.py -p $j -b $BATCH_SIZE >> out.txt
	done
done




#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;BATCH_SIZE (InfluxDB)
#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;X (TimescaleDB)