import pprint
import urllib, json
import pymongo
import os


def MakeDataBase():
#This part reads the json file from the github link provided
#Then stores it in an array called data
	url = "https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json"
	response = urllib.urlopen(url)
	data = json.loads(response.read())

#Now we demonstrate how to create that data in our own mongodb database
	
	client = pymongo.MongoClient()
	db = client.AirportsData
	db.AirportsData.insert(data)




#----------------------------------------------------------
def Search(category, value):
	client = pymongo.MongoClient()
	db = client.AirportsData
	specific = db.AirportsData.find_one({category : value}) #returns the object with those credentials
	print('The properties are: \n')
	pprint.pprint(specific)




#----------------------------------------------------------
def Update():
	print("Enter the properties of the new Airport you want to add: ")
	code = raw_input('Enter the code: ')
	lat = raw_input('Enter the latitude: ')
	lon = raw_input('Enter the longitude: ')
	name = raw_input('Enter the name: ')
	city = raw_input('Enter the city: ')
	state = raw_input('Enter the state: ')
	country = raw_input('Enter the country: ')
	woeid = raw_input('Enther the woeid: ')
	tz = raw_input('Enter the tz: ')
	phone = raw_input('Enter the phone: ')
	email = raw_input('Enter the email: ')
	url = raw_input('Enter the url: ')
	runway = raw_input('Enter the runway length: ')
	elev = raw_input('Enter the elevation: ')
	icao = raw_input('Enter the icao: ')
	flights = raw_input('Enter the direct_flights: ')
	carrierss = raw_input('Enter the carriers: ')

	newone = {"code" : code, "lat":lat, "lon" : lon, "name":name, "city":city,
				"state":state, "country":country, "woeid":woeid, "tz": tz, "phone":phone,
				"email":email, "url":url,"runway_length": runway, "elev":elev, "icao":icao,
				"direct_flights":flights, "carriers":carrierss}

	client = pymongo.MongoClient()
	db = client.AirportsData
	db.AirportsData.insert(newone)




if __name__ == '__main__':
	#os.system("mongod") #need this to connect to client so that we can enter our data
	MakeDataBase()
	category = raw_input("Are you looking for a city, a code, an airport name, etc. ? ")
	value = raw_input("What is the keyword of what you are looking for? ")
	Search(category, value)
	Update()




