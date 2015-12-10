import json
import datetime
from pprint import pprint

def dayConverter(timestamp):
	data = {}
	date = datetime.datetime.fromtimestamp(timestamp/ 1000.0)
	data["day"] = date.isoweekday()  
	data["hour"] = date.hour
	data["minute"] =date.minute
	data["complete_time"] = str(date.hour) + ":" + str(date.minute)
	data["date"] = str(date.month)+"," + str(date.day)+ "," + str(date.year)
	return data

picDict={}
fin= open('../flickr1k-photos', 'r')
for line in fin:
	data = json.loads(line)
	if not data["captureDevice"]:
		continue
	del data["description"]
	del data["downloadUrl"] #what we want for pic
	del data["extension"]
	del data["favorites"]
	del data["pageUrl"]
	del data["title"]
	del data["userTags"]
	data["state"] =""
	data["county"] =""
	data["dateUploadedDets"]=dayConverter(data["dateUploaded"])
	picDict[data["id"]] = data

with open('../filteredPhotos', 'w') as outfile:
    json.dump(picDict, outfile)
		
