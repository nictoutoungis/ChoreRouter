#!/usr/bin/env python3

from googlemaps.client import Client
from googlemaps.distance_matrix import distance_matrix
import requests, json, secret
import re

#--------- All comprehension stuff from Virdin ---------------

api_key = secret.api_key
gmaps = Client(api_key)


def main():

	choreList = ["laundry", "food", "supermarket", "mechanic"]

	addressList = generateAddressList(choreList)	
	
	distance = findDistance(addressList[0][1], addressList[0][1])

	dictList = generateDictList(addressList)

	graph = makeDict(dictList)

	mst = prim(graph)


def generateAddressList(choreList):

	listOfBusinesses = list()

	for i in choreList:

		individualBusiness = list()

		url =f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={i}&inputtype=textquery&fields=formatted_address,name&key={api_key}"
		r = requests.get(url)
		info = r.json()
		
		name = info["candidates"][0]["name"]
		address = info["candidates"][0]["formatted_address"]

		individualBusiness.append(name)
		individualBusiness.append(address)

		listOfBusinesses.append(tuple(individualBusiness))

	return listOfBusinesses


def findDistance(location1, location2):

	distanceJSON = distance_matrix(gmaps, location1, location2)
	distance = distanceJSON["rows"][0]["elements"][0]["distance"]["text"]
	distanceNum = re.findall(r"^\d*.?\d*", distance)

	return float(distanceNum[0]) * 1000


def generateDictList(addressList):

	dictList = list()

	for i in range(len(addressList)):

		tempTuple = tuple()
		distanceList = list()

		for j in range(len(addressList)):

			distance = findDistance(addressList[i][1], addressList[j][1])

			if addressList[i][1] != addressList[j][1]:

				tempTuple = (addressList[j][0], distance)
				distanceList.append(tempTuple)

		tempTuple = (addressList[i][0], distanceList)
		
		dictList.append(tempTuple)

	return dictList


'''
Performs Prim's Algorithm 
Returns a two-element tuple
	first element: Minimum Spanning Tree of the graph (a list of just the business names)
	second element: Distance to fully traverse that Minimum Spanning Tree
'''

def makeDict(dictList):

	addressDict = {tup[0]: tup[1] for tup in dictList}

	return addressDict


def prim(graph):

	distanceList = [[tup for tup in graph[key]] for values in graph.values()]

	# distanceList = [key for key in graph]

	print(distanceList)
	print(graph.values())
	
	# minimumSpanningTree = list()
	# minDistance

	# for key in graph:

	# for i in graph.values():

	# 	print(i)

		




'''
This is complete. Don't touch it.
'''
# def main():
# 	addressList = generateAddressList(choreList)
# 	dictlist = generateDictList(addressList)
# 	graph = {node[0]: node[1] for node in dictlist}
# 	tree, totalDistance = prim(dictlist[0][0], graph)
# 	print(f'{tree}\nThis path is {totalDistance} meters long')
# 	return

if __name__ == "__main__":
	main()
# Uncomment when ready!
#main()