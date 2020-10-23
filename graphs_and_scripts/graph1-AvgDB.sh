#!/bin/bash

#for method in ER OPPcycles #FixOpt
for database in InfluxDB TimescaleDB
do
	for size in 1000 10000 100000 1000000
	do
		echo "database: "$database " size: "$size
		outTemp="avgTime-$database-$size.dat"
		avgInsert=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$3; count+=1} END {print sum/count}'  \
		../out.txt)
		avgDel=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$4; count+=1} END {print sum/count}'  \
		../out.txt)
		avgGetDev=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$5; count+=1} END {print sum/count}'  \
		../out.txt)
		echo $avgInsert $avgDel $avgGetDev > $outTemp
	done
done

string=$(echo "#AvgTime InfluxDB-avgInsert InfluxDB-avgDel InfluxDB-avgGetDev TimescaleDB-avgInsert TimescaleDB-avgDel TimescaleDB-avgGetDev")
echo $string >> AVG-DB.out
for size in 1000 10000 100000 1000000
do
	avgIDB=$(cat avgTime-InfluxDB-$size.dat)
	avgTDB=$(cat avgTime-TimescaleDB-$size.dat)

	string=$(echo $size $avgIDB $avgTDB $avgGetDevTDB)
	echo $string >> AVG-DB.out

	rm avgTime-InfluxDB-$size.dat
	rm avgTime-TimescaleDB-$size.dat
done