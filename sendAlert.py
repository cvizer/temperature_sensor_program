import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time
import pymongo
from pymongo import MongoClient

cluster = MongoClient("")
db = cluster["test"]
collection = db["test"]

starttime = time.time()
while True:

    postCount = collection.count()
    latestTemp = postCount - 1

    results = collection.find({"_id":latestTemp})

    for result in results:
        testNum = result["temperature"]

    # function to send text alert if temp too high.
    def sendHighSMS(testNum):
        account_sid = ""
        auth_token = ""

        client = Client(account_sid, auth_token)

        client.messages.create(
            to="",
            from_="",
            body="Warning: Incoming temperature too high. It's {} degrees.".format(testNum)
        )

    # function to send text alert for temp too low.
    def sendLowSMS(testNum):
        account_sid = ""
        auth_token = ""

        client = Client(account_sid, auth_token)

        client.messages.create(
            to="",
            from_="",
            body="Warning: Incoming temperature too low. It's {} degrees.".format(testNum)
        )

    # Run sendHighSMS or sendLowSMS if temperature is too high or too low.
    def sendSms(testNum):
        if testNum > 199:
            sendHighSMS(testNum)
        elif testNum < 180:
            sendLowSMS(testNum)

    sendSms(testNum)

    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
