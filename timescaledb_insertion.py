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

DEFAULT_PROBES = 0
DEFAULT_DEVICES = 0

class DataBase():
    def __init__ (self):
        #connect to the db
        self.conn = pg2.connect(
            host = "localhost",
            database = "probemon",
            user = "postgres",
            password = "123")    

    # serie temporal - tempo de fila
    def insertion(self, p, d):

        print("p: " + str(p) + " d: " + str(d))

        #cursor
        cur = self.conn.cursor()
        
        #table's name
        table_name = "telemetry_data"

        #execute query
        query = sql.SQL("drop table telemetry_data")
        cur.execute(query)
        query = sql.SQL("create table if not exists telemetry_data (timestamptz TIMESTAMPTZ, device INTEGER not null, queue_time INTEGER not null, process_time INTEGER not null)")
        cur.execute(query)
        data = []
        for _ in range(p):
            for d in range(d):
                #query = sql.SQL("insert into telemetry_data (timestamptz, device, queue_time, process_time) values (%s, %s, %s, %s)").format(sql.Identifier(table_name))
                timestamptz = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
                queue_time = random.randrange(1, 100)
                process_time = random.randrange(1, 200)
                tup = (timestamptz, d, queue_time, process_time)
                data.append(tup)
                #cur.execute(query, (timestamptz, d, queue_time, process_time))
        
        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s)", x).decode("utf-8") for x in data)
        start = int(round(time.time()) * 1000)
        cur.execute("INSERT INTO telemetry_data VALUES " + args_str)
        end = int(round(time.time()) * 1000)
        self.conn.commit()
        cur.close()
        print("Total time: " + str(end - start) + "ms")

    def close_conn(self):
        #close the connection
        self.conn.close()



def main():

    parser = argparse.ArgumentParser(description='TimescaleDB run manager')
    parser.add_argument("--probes", "-p", help="Number of probes", default=None, type=int)
    parser.add_argument("--devices", "-d", help="Number of devices", default=None, type=int)
    #parser.add_argument("--batchsize", "-b", help="Batch size", default=DEFAULT_BATCH_SIZE, type=int)

    args = parser.parse_args()
    
    #create connection to timescaledb
    db = DataBase()

    #queries
    db.insertion(args.probes, args.devices)

	#close connection
    db.close_conn()


if __name__ == "__main__":
    sys.exit(main())
