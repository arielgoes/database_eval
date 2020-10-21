#!/usr/bin/python3.7
from influxdb import InfluxDBClient
import random
import time
from datetime import datetime

DEFAULT_BATCH_SIZE = 5000

client = InfluxDBClient(host='localhost', port=8086)

#overwrites old database
client.drop_database("ProbeMon")
client.create_database("ProbeMon")

#use recreated database
client.switch_database("ProbeMon")


#insert dumb data
data = []

for i in range(5000): #instant of time
    for j in range(200): #number of devices
        #q_time = random.randint(1, 15) #time in ms
        #p_time = random.randint(5, 200) #time in ms
        di_data =   {"measurement": "telemetry_data", 
                    "tags": {"id" : j},
                    "time": int(time.time_ns()) - random.randint(1,9999),
                    "fields": {"queue_time": random.randint(1, 10), "process_time": random.randint(1,10)}}
        data.append(di_data)                   

start = int(round(time.time()) * 1000)
if(b > i*j):
    print("BATCH_SIZE TOO LARGE, MAXIMUM VALUE IS (PROBES * DEVICES) = %d, USING %d", i*j, DEFAULT_BATCH_SIZE)
    b = DEFAULT_BATCH_SIZE
elif(b <= 0):
    print("BATCH_SIZE TOO SMALL, MINIMUM VALUE IS 1, USING %d", DEFAULT_BATCH_SIZE)
    b = DEFAULT_BATCH_SIZE
client.write_points(data, batch_size=b)
end = int(round(time.time()) * 1000)
print("Total time: " + str(end - start) + "ms")

def if __name__ == "__main__":
    pass
