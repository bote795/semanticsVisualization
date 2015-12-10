$(document).ready(function(){
  $.getJSON( "filteredPhotos", function( data ) {
    var formatedData= data;
    console.log(formatedData);
    var str = JSON.stringify(formatedData, undefined, 4);
    output(str);
  });
});

function output(inp) {
    document.body.appendChild(document.createElement('pre')).innerHTML = inp;
}
function formatData (contents) {
  var picDict={};
  var tagsDict={};
  for (var i = 0; i < contents.length; i++) {
  	console.log(i);
    //console.log(contents[i]);
  	var temp =JSON.parse(contents[i]);
  	if (temp.captureDevice ==="") 
  	{
  	 continue;
  	};
  	console.log(JSON.parse(contents[i]));
  	delete temp.description;
  	delete temp.downloadUrl;
  	delete temp.extension;
  	delete temp.favorites;
  	delete temp.pageUrl;
  	delete temp.title;
  	delete temp.userTags;
  	temp.state="";
  	temp.county="";
  	temp.dateUploadedDets=dayConverter(temp.dateUploaded);
  	tagsFrequency(tagsDict, temp);
  	console.log(temp);
  	picDict[temp.id]=temp;
  };
  var str = JSON.stringify(picDict, undefined, 4);
  output(str);
  console.log(tagsDict);
}
function tagsFrequency (tagsDict, temp) {
	for (var g = 0; g < temp.machineTags.length; g++) {
  		if (temp.machineTags[g].tag in tagsDict)
  		{
  			tagsDict[temp.machineTags[g].tag ]++;
  			tagsDict[temp.machineTags[g].tag ]++;
  		} 
  		else
  		{
  			tagsDict[temp.machineTags[g].tag ]=1;
  		};
  	};
}
function dayConverter(date)
{
	var time= {};
	var d = new Date();
	d.setTime(date);
	console.log(d);
	time.day= d.getDay();
	time.hour =d.getHours();
	time.minutes= d.getMinutes();
	time.complete_time = d.getHours()+":"+d.getMinutes();
	time.date = d.getMonth()+"," +d.getDate()+ "," +d.getFullYear();
	return time;
}