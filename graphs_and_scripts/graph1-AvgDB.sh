#!/bin/bash

#for method in ER OPPcycles #FixOpt
for database in InfluxDB TimescaleDB
do
	for size in 1000 10000 100000 1000000
	do
		echo "database: "$database " size: "$size
		outTemp="avg-std-time-$database-$size.dat"
		avgInsert=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$3; count+=1} END {print sum/count}' \
		../out.txt)
		stdInsert=$(awk -F";" -v num=${size} -v db=${database} '$1==db && $2==num {delta = $3 - avg; avg += delta / NR; mean2 += delta * ($3 - avg); } \
		END { print sqrt(mean2 / (NR-1)); }' ../out.txt)
		avgDel=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$4; count+=1} END {print sum/count}' \
		../out.txt)
		stdDel=$(awk -F";" -v num=${size} -v db=${database} '$1==db && $2==num {delta = $4 - avg; avg += delta / NR; mean2 += delta * ($4 - avg); } \
		END { print sqrt(mean2 / (NR-1)); }' ../out.txt)
		avgGetDev=$(awk --field-separator=";" -v num=${size} -v db=${database} '$1==db && $2==num {sum+=$5; count+=1} END {print sum/count}' \
		../out.txt)
		stdGetDev=$(awk -F";" -v num=${size} -v db=${database} '$1==db && $2==num {delta = $5 - avg; avg += delta / NR; mean2 += delta * ($5 - avg); } \
		END { print sqrt(mean2 / (NR-1)); }' ../out.txt)
		echo $avgInsert $avgDel $avgGetDev $stdInsert $stdDel $stdGetDev > $outTemp
	done
done

string=$(echo "#AvgTime IDB-avgInsert IDB-avgDel IDB-avgGetDev TDB-avgInsert TDB-avgDel TDB-avgGetDev IDB-stdInsert IDB-stdDel IDB-stdGetDev TDB-stdInsert TDB-stdDel TDB-stdGetDev")
echo $string >> AVG-DB.out
for size in 1000 10000 100000 1000000
do
	allIDB=$(cat avg-std-time-InfluxDB-$size.dat)
	allTDB=$(cat avg-std-time-TimescaleDB-$size.dat)

	string=$(echo $size $allIDB $allTDB)
	echo $string >> AVG-DB.out

	rm avg-std-time-InfluxDB-$size.dat
	rm avg-std-time-TimescaleDB-$size.dat
done