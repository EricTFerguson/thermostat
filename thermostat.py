import pigpio
import DHT22
from time import sleep
import csv
import datetime
import pandas as pd
import bokeh
from twilio.rest import Client

#Open file read/write objects
f = open("data.csv", 'r+')
csv_writer = csv.writer(f, delimiter=',', quotechar='"')
html_writer = open("/var/www/html/index.html", 'w')

with open('login.txt', 'r') as f:
	account_sid = f.readline().strip()
	auth_token = f.readline().strip()

client = Client(account_sid, auth_token)


#Initiate the GPIO for pigpio
pi = pigpio.pi()
 
#Setup the sensor
dht22 = DHT22.sensor(pi, 4)

#trigger the pi 3x to flush out the initial bad readings
csv_writer.writerow([" ","Humidity","Temperature"])

#Set sleeptime to be above 2 seconds
sleepTime = 3

#flush out garbage readings
for i in range(0,2):
	dht22.trigger()
	sleep(sleepTime)

def read():
	#Get a new reading
	dht22.trigger()
	#Save our values
	humidity = float(dht22.humidity())
	temp = float(dht22.temperature())
	return(humidity, temp)

def check_readings(humidity, temperature):
	
	if humidity > 50.0 or humidity < 10.0:
		
		humidity = "%.2f" % humidity
		
		message = client.messages.create(
			to="+14435049478",
			from_="+14436489902",
			body="Humidity is " + humidity)

	if temperature > 50.0 or temperature < 5.0:
		
		temperature = "%.2f" % temperature
		
		message = client.messages.create(
			to="+4435049478",
			from_="+14436489902",
			body="Temperature is " + temperature)

while True:
	
	humidity, temperature = read()
		

	check_readings(humidity, temperature)
	humidity = '%.2f' % humidity
	temperature = '%.2f' % temperature


	html_content = """
	<head>
		<link rel="stylesheet" href="main.css">
	</head>
	<body>
	
	<h1>Temperature and Humidity Readings</h1>
	<h1>EcoPi Solutions</h1>
	<p>Temperature: {temperature}<br>
	Humidity: {humidity}<br>
	
	<a href='histeve.html'> Say hi to steve</a>
	</p>
	</body>

	""".format(temperature=temperature, humidity=humidity)

	now = datetime.datetime.now()
	print("Humidity is: " + humidity + "%")
	print("Temperature is: " + temperature + "C")
	csv_writer.writerow([now, str(humidity), str(temperature)])
	
	html_writer.seek(0)
	html_writer.write(html_content)
	
	sleep(sleepTime)
	

