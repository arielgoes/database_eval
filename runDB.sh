#!/bin/bash

echo "Insertions = <probes> * <devices>"
echo "Usage: <repetitions> <batch_size> <probes> <devices>"
read N BATCH_SIZE PROBES DEVICES

if [[ $N -le 0 || $PROBES -le 0 || $DEVICES -le 0 ]]; then
	echo "Usage: <N>, <probes> and <devices> must be greater than 0"
	exit 1
fi

for((j=10;j<=$PROBES;j*=10)); do
	for((k=10;k<=$DEVICES;k*=10)); do
		for((i=0;i<$N;i++)); do
			#echo "Execution #" $i
			python3.7 run_timescaledb.py -p $j -d $k
		done
	done
done

for((j=10;j<=$PROBES;j*=10)); do
	for((k=10;k<=$DEVICES;k*=10)); do
		for((i=0;i<$N;i++)); do
			#echo "Execution #" $i
			python3.7 run_influxdb.py -p $j -d $k -b $BATCH_SIZE
		done
	done
done




#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;BATCH_SIZE (InfluxDB)
#PROBES;DEVICES;TOTAL_INSERTIONS;INSERTION_TIME;DELETION_TIME;X (TimescaleDB)