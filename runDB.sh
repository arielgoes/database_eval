#!/bin/bash

echo "Choose the DBMS to run experiments: "
echo "[1] InfluxDB -- [2] TimescaleDB -- [3] PostgreSQL"
read -p 
case RUN in
	1) echo "[1] InfluxDB"
