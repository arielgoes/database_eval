import psycopg2 as pg2
from psycopg2 import sql
import datetime
import random
import pytz
import time
from threading import Thread
from subprocess import check_output
import subprocess

class DataBase:
    def __init__ (self):
        #connect to the db
        self.conn = pg2.connect(
            host = "localhost",
            database = "probemon",
            user = "postgres",
            password = "123")    

    # serie temporal - tempo de fila
    def insertion(self):
        #cursor
        cur = self.conn.cursor()
        
        #table's name
        table_name = "telemetry_data"

        #execute query
        query = sql.SQL("drop table telemetry_data")
        cur.execute(query)
        query = sql.SQL("create table if not exists telemetry_data (timestamptz TIMESTAMPTZ, queue_time INTEGER not null, process_time INTEGER not null)")
        cur.execute(query)
        
        for _ in range(10000):
            query = sql.SQL("insert into telemetry_data (timestamptz, queue_time, process_time) values (%s, %s, %s)").format(sql.Identifier(table_name))
            timestamptz = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
            queue_time = random.randrange(1, 100)
            process_time = random.randrange(1, 200)
            cur.execute(query, (timestamptz, queue_time, process_time))
        self.conn.commit()
        cur.close()


    def close_conn(self):
        #close the connection
        self.conn.close()



def main():
    db = DataBase()

    #queries
    db.insertion()

    #close connection
    #db.close_conn()


if __name__ == "__main__":
    main()