import urllib.parse
import requests

history = []

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "c9JC3qMQE3JTIgLkY6Wz2YqmUfpfK1bd"

def getroute():

	orig = input("Origin location (City, Country): ")
	if orig == "quit" or orig == "q":
 		return

	dest = input("Destination location (City, Country): ")
	if dest == "quit" or dest == "q":
 		return 

	url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
	print("Connecting to " + url)

	json_data = requests.get(url).json()
	json_status = json_data["info"]["statuscode"]

	if json_status == 0:
		print("API Status: " + str(json_status) + " = A successful route call.\n")
		print("=============================================")
		print("Directions from " + (orig) + " to " + (dest))
		print("Trip Duration: " + (json_data["route"]["formattedTime"]))
		print("Kilometers: " + "{:.2f}".format(json_data["route"]["distance"] * 1.61))
		print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
		print("=============================================")
		
		for each in json_data["route"]["legs"][0]["maneuvers"]:
			print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

		history.append({"orig":orig, "dest":dest})

	elif json_status == 402:
		print("**********************************************")
		print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
		print("**********************************************\n")
	elif json_status == 611:
		print("**********************************************")
		print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
		print("**********************************************\n")
	else:
		print("************************************************************************")
		print("For Staus Code: " + str(json_status) + "; Refer to:")
		print("https://developer.mapquest.com/documentation/directions-api/status-codes")
		print("************************************************************************\n")

def gethistory():
	print("Search history: \n")
	for each in history:
		print(each["orig"] + " -> " + each["dest"] + "\n")

def checkfuel():
	fuel = float(input("Your fuel in Ltr: "))
	consum = float(input("Your fuel consumption in Ltr/100 Km: ")) / 100

	orig = input("Origin location (City, Country): ")
	if orig == "quit" or orig == "q":
 		return

	dest = input("Destination location (City, Country): ")
	if dest == "quit" or dest == "q":
 		return 

	url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
	print("Connecting to " + url)

	json_data =  requests.get(url).json()
	json_status = json_data["info"]["statuscode"]

	if json_status == 0:
		history.append({"orig":orig, "dest":dest})

		if (fuel > json_data["route"]["distance"] * 1.61 * consum):
			print("Sure you can go :)\n")
		else:
			print("Sorry, you need more fuel to go (" + str(json_data["route"]["distance"] * 1.61 * consum) + ") :(\n")
	elif json_status == 402:
		print("**********************************************")
		print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
		print("**********************************************\n")
	elif json_status == 611:
		print("**********************************************")
		print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
		print("**********************************************\n")
	else:
		print("************************************************************************")
		print("For Staus Code: " + str(json_status) + "; Refer to:")
		print("https://developer.mapquest.com/documentation/directions-api/status-codes")
		print("************************************************************************\n")


def funcerr():
	print("No such function in menu!\n")

mainmenu = ("Main menu", "1) Get route", "2) Get history", "3) Check for fuel enough", "4) Exit")
menuswitch = { 1:getroute, 2:gethistory, 3:checkfuel }

while True:

	for each in mainmenu:
		print(each)

	func = int(input("> "))
	if func == 4: break;
	else: menuswitch.get(func, funcerr)()