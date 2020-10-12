# database_eval
## Requirements
### InfluxDB
- Install Python 3.7: "sudo apt install python3.7"
- Install library InfluxDBClient: "sudo python3.7 -m pip install influxdb"

Run: python3.7 <\file.py>

## TimeScaleDB
- Install Python 3.7: "sudo apt install python3.7"  
- Install PostgreSQL 11:  
    "wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -"  
    "sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'"  
    "sudo apt-get update"  
    "sudo apt-get install postgresql-11"  
- Install TimescaleDB 1.7.4:  
    "sudo add-apt-repository ppa:timescale/timescaledb-ppa"  
    "sudo apt-get update"  
    "sudo apt install timescaledb-postgresql-11"  
- Setup Postgre to accept TimescaleDB library:  
    "sudo bash"  
    "echo "shared_preload_libraries = 'timescaledb'" >> /etc/postgresql/11/main/postgresql.conf"
- Install Psycopg2: "sudo python3.7 -m pip install psycopg2-binary"  

Set user postgres:
1. sudo su -l postgres
2. psql
3. \password postgres
4. 123
5. CREATE DATABASE ProbeMon;
6. \c probemon
7. sudo gedit /etc/postgresql/11/main/postgresql.conf (change "shared_preload_libraries= ''" to "shared_preload_libraries= 'timescaledb'", including at the end of the file)
8. sudo su -l postgres
9. psql
10. \c probemon
11. CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;