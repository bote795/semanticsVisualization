import json
from pprint import pprint
#return season of the year based of timestamp
def season(timestamp):
	seasons = {
        'March': "Spring",
        'April': "Spring",
        'May': "Spring",
        'June': "Summer",
        'July': "Summer",
        'August': "Summer",
        'September': "Autumn",
        'October': "Autumn"
        'November': "Autumn",
        'December': "Winter ",
        'January': "Winter ",
        'February': "Winter ",
    }
	date = datetime.datetime.fromtimestamp(timestamp/ 1000.0)
	return seasons[date.month]

def renameDevice(deviceName):
	nameSplit=deviceName.split()
	if len(nameSplit) >= 2:
		return nameSplit[0] +" "+ nameSplit[1]
	else:
		return deviceName
tagFreqDict={}
tagDeviceDict={}
devceFreqDict={}
picDict={}
fin= open('../../flickr100k-photos', 'r')
for line in fin:
	data = json.loads(line)
	if not data["captureDevice"]:
		continue
	data["captureDevice"]= renameDevice(data["captureDevice"])
	if data["captureDevice"] in devceFreqDict:
		devceFreqDict[data["captureDevice"] ] += 1
	else:
		devceFreqDict[data["captureDevice"] ] = 1


	for item in data["machineTags"]:
		if item["tag"] in tagFreqDict:
			tagFreqDict[item["tag"]]+=1
			tagCaptureDict= tagDeviceDict[item["tag"]]  #retrieve dict of capturedevices
			if data["captureDevice"] in tagCaptureDict:
				tagCaptureDict[data["captureDevice"]]+=1	#add one to the freq of that capture device for that tag
			else:
				tagCaptureDict[data["captureDevice"]] =1 
			tagDeviceDict[item["tag"]] = tagCaptureDict #save it bk
		else:
			picDict[item["tag"]]=data["downloadUrl"]
			tagCaptureDict={} # dict of captureDevices for that specific tag
			tagCaptureDict[data["captureDevice"]] =1 #set first device to default 1
			tagDeviceDict[item["tag"]] = tagCaptureDict #save it
			tagFreqDict[item["tag"]]=1

print (str(len(tagFreqDict)))
print (sorted(tagFreqDict, key=tagFreqDict.get, reverse=True)[:10])
print (str(len(devceFreqDict)))
print (sorted(devceFreqDict, key=devceFreqDict.get, reverse=True)[:10])

FinalTagDict={}
uniqueDeviceMaxDict={}
TagsDict={}
TagsDict["name"] = "tags"
children=[]
for key, value in tagFreqDict.items():
	if len(tagDeviceDict[key]) == 1:
		print ("Key:"+ key + " : "+str(value))
		pprint (tagDeviceDict[key])

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
	children.append({"name": key , "size": value, "url": picDict[key]})
TagsDict["children"]= children
pprint(TagsDict);
print (len(children))
# with open('../tags', 'w') as outfile:
#    json.dump(TagsDict, outfile)
print ("Job is complete")