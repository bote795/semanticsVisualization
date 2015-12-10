import json
import datetime

from pprint import pprint
#return season of the year based of timestamp
def Time(timestamp):
	seasons = {
        '3'  : 'Spring',
        '4'  : "Spring",
        '5'  : "Spring",
        '6'  : "Summer",
        '7'  : "Summer",
        '8'  : "Summer",
        '9'  : "Autumn",
        '10' : "Autumn",
        '11' : "Autumn",
        '12' : "Winter ",
        '1'  : "Winter ",
        '2'  : "Winter ",}
	try:
		date = datetime.datetime.fromtimestamp(timestamp/ 1000.0)
	except:
		print (timestamp)
	
	return {'season': seasons[str(date.month)] , 'HourOfDay': date.hour}

def renameDevice(deviceName):
	nameSplit=deviceName.split()
	if len(nameSplit) >= 2:
		return nameSplit[0] +" "+ nameSplit[1]
	else:
		return deviceName
def updateDict(dictTemp, key):
	if key in dictTemp:
		dictTemp[key]+=1
	else:
		dictTemp[key]=1
def UpdateSeasonAndTime(sAndTDict, time):
	updateDict(sAndTDict["season"],time["season"])
	updateDict(sAndTDict["HourOfDay"],time["HourOfDay"])

tagFreqDict={}
tagDeviceDict={}
devceFreqDict={}
timeFreqDict={} #key : tag value: dict [dict["season"], dict["HourOfDay"]]
picDict={}
fin= open('../../flickr100k-photos', 'r')
for line in fin:
	data = json.loads(line)
	if not data["captureDevice"] or str(data["dateTaken"])[0] == '-':
		continue
	data["captureDevice"]= renameDevice(data["captureDevice"])
	updateDict(devceFreqDict,data["captureDevice"])
	for item in data["machineTags"]:
		time= Time(data["dateTaken"])
		#if tag already stored
		if item["tag"] in tagFreqDict:
			tagFreqDict[item["tag"]]+=1
			UpdateSeasonAndTime(timeFreqDict[item["tag"]],time)
			updateDict(tagDeviceDict[item["tag"]], data["captureDevice"]) #update captureDevice Freq
		else:
			picDict[item["tag"]]=data["downloadUrl"]
			tagCaptureDict={} # dict of captureDevices for that specific tag
			tagCaptureDict[data["captureDevice"]] =1 #set first device to default 1
			tagDeviceDict[item["tag"]] = tagCaptureDict #save it
			tagFreqDict[item["tag"]]=1
			timeFreqDict[item["tag"]]= {"season": {time["season"]: 1}, "HourOfDay": {time["HourOfDay"]: 1}}

print (str(len(tagFreqDict)))
print (sorted(tagFreqDict, key=tagFreqDict.get, reverse=True)[:10])
print (str(len(devceFreqDict)))
print (sorted(devceFreqDict, key=devceFreqDict.get, reverse=True)[:10])

FinalTagDict={}
uniqueDeviceMaxDict={}
TagsDict={}
TagsDict["name"] = "tags"
children=[]
tagSortedArray=sorted(tagFreqDict, key=tagFreqDict.get, reverse=True) #highest at the top
for key in tagSortedArray:
	value= tagFreqDict[key]
	if len(tagDeviceDict[key]) == 1:
		print ("Key:"+ key + " : "+str(value))
		pprint (tagDeviceDict[key])
	seasonKey=sorted(timeFreqDict[key]["season"], key=timeFreqDict[key]["season"].get,reverse=True)[:1]
	seasonKey=seasonKey[0]
	HourKey=sorted(timeFreqDict[key]["HourOfDay"], key=timeFreqDict[key]["HourOfDay"].get, reverse=True)[:1]
	HourKey=HourKey[0]
	completeTempTagDict ={}
	completeTempTagDict["Freqency"] = value
	maxKey=max(tagDeviceDict[key],key= tagDeviceDict[key].get)
	temp=[]
	if maxKey in uniqueDeviceMaxDict:
		temp=uniqueDeviceMaxDict[maxKey ]
		temp.append({"name": key, "size": tagDeviceDict[key][maxKey]})
	else:
		temp.append({"name": key, "size": tagDeviceDict[key][maxKey]})
		uniqueDeviceMaxDict[maxKey] = temp
	
	completeTempTagDict["MaxDevice"]  = { "name":maxKey, "num":  tagDeviceDict[key][maxKey] }
	FinalTagDict[key]=completeTempTagDict

	children.append({"name": key , "size": value, "url": picDict[key], 
		"season": {"name": seasonKey, "freq": timeFreqDict[key]["season"][seasonKey]} ,
		"HourOfDay": {"time": HourKey, "freq":timeFreqDict[key]["HourOfDay"][HourKey] },
		"device": completeTempTagDict["MaxDevice"]
		})
TagsDict["children"]= children
pprint(TagsDict);
print (len(children))
with open('../FullData', 'w') as outfile:
   json.dump(TagsDict, outfile)
print ("Job is complete")