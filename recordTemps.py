import os
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("")
db = cluster["test"]
collection = db["test"]

newest = collection.find({}).limit(1).sort([('$natural', pymongo.DESCENDING)])

for y in newest:
    postCount = y["_id"]

starttime = time.time()
while True:

    val1 = ""

    def sensor():
        for i in os.listdir('/sys/bus/w1/devices'):
            if i != 'w1_bus_master1':
                ds18b20 = i
        return ds18b20

    sensor = sensor()

    def read(ds18b20):
        location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        celsius = temperature / 1000
        farenheit = (celsius * 1.8) + 32
        return celsius, farenheit

    def getTemp(ds18b20):
        if read(ds18b20) != None:
            val1 = read(ds18b20)[1]
            val1 = str(val1)
            return val1

    val1 = getTemp(sensor)
    val1 = float(val1)
    val2 = int(val1)
    val1 = str(val2)

    oldest = collection.find({}).limit(1)

    for u in oldest:
        firstId = u["_id"]

    myQuery = { "_id": firstId }
    # Deletes the oldest record in the database, so that it doesn't keep getting bigger and bigger.
    collection.delete_one(myQuery)

    postCount +=1

    post = {"_id":postCount, "temperature":val2, "time": datetime.utcnow()}

    collection.insert_one(post)

    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
