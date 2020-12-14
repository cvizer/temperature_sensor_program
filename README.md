# Temperature Monitoring Program

## Purpose

> Monitor temperature, store temperature results in a MongoDB Collection, and receive text alerts if the temperature is out of spec.

## Description

This is a 2 part program. One part ([recordTemps.py](https://github.com/cvizer/temperature_sensor_program/blob/main/recordTemps.py)) obtains a temperature reading from a sensor every 60 seconds and records that temperature into a database on MongoDB. The second part ([sendAlert.py](https://github.com/cvizer/temperature_sensor_program/blob/main/sendAlert.py)) checks the latest temperature reading every 60 seconds and sends a text message to alert you if the temperature is out of spec.

> See a real-time graph that represents the program running right now: https://cvizer.github.io/temp-monitoring-website/pinkGraph/examples/dashboard.html

---

## You Will Need

* A temperature sensor (I used the ds18b20 with a Raspberry Pi).

* A collection set up on MongoDB to store the temperature readings.

* A Twilio account.

---

## How To Use

First, we will want to start recording some temperature readings in our database. Edit lines 7, 8, & 9 of the recordTemps.py file to add in your own MongoDB URL, Cluster, and Collection.

```python
    cluster = MongoClient("<<MongoDB URL>>")
    db = cluster["<<Your Cluster>>"]
    collection = db["<<Your Collection>>"] 
```

Now run the program from the command line:

`python3 recordTemps.py`

 Now we're ready to modify the sendAlert.py file. Edit lines 8, 9, & 10 with your MongoDB URL, Cluster, and Collection, just like we did in the recordTemps.py file.

Modify lines 25, 26, 38, & 39 to add in your Twilio Account SID and Auth Token.

```python
    def sendHighSMS(testNum):
        account_sid = "<<Your Account SID>>"
        auth_token = "<<Your Auth Token>>"
```

We'll also want to add in our "to" and "from" phone numbers. The "to" phone number should be the phone number that you want the text message alerts to be sent to. *Note that you'll have to verify this phone number with Twilio in order to receive messages. The "from" phone number will be your Twilio phone number.

```python
    client.messages.create(
            to="<<Your Phone Number>>",
            from_="<<Your Twilio Phone Number>>",
```

The last thing we'll need to change is the temperatures at which you want to be alerted for. I set mine to anything higher than 199 degrees Fahrenheit or lower than 180 degrees Fahrenheit (as I am using this on an outdoor wood furnace), but you can adjust accordingly.

```python
    def sendSms(testNum):
        if testNum > 199:
            sendHighSMS(testNum)
        elif testNum < 180:
            sendLowSMS(testNum)
```

Finally, we're ready to run the second program from the command line, as well. Either open up another command line window, or run this on another computer:

`python sendAlert.py`

I ran the recordTemp.py program using "python3", whereas I ran the sendAlert.py program using "python", but this is due to the fact that I'm running them on two different computers with different versions of Python on them. Use whichever corresponds to the version of Python you're using.

You're up and running! You will now receive a text message alerting you if your outdoor wood furnace gets too hot or cold and needs attention.

---

## To Do

* Implement UI

## Author Info

- Github - [github.com/cvizer](https://github.com/cvizer)
- Email - <chelseavizer@yahoo.com>

[Back To Top](#temperature-monitoring-program)
