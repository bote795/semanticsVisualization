// Join the photos and users into one dataset, using Node.js

var fs = require('fs'); // for file system operations
var readline = require('readline'); // for reading a file line by line 

// Loads a file line by line, and parse each line into an object. Skip lines
// that do not parse correctly.
//
// (Note that this is an asynchronous function, as many other Node.js functions:
// the call to this function will return immediately without the result; the
// result will be communicated through the callabck function.)
//
// - filePath: the path to the file to read.
//
// - callback: the function that will be called when all the lines are read and
// parsed, or when a fatal error happens. should have the following parameters:
//     - err: the error object if a fatal error happened, otherwise null.
//     - objs: the Array of objects parsed from lines in the file.
function loadLinesAsObjs(filePath, callback) {
  var readStream = fs.createReadStream(filePath);

  // the 'error' event happens when the filePath is invalid, or there is
  // permission issue, etc.
  readStream.on('error', callback);

  // the 'open' event happens when the stream is ready to read.
  // the anonymous function is called when the 'open' event happens.
  readStream.on('open', function() {
    var rl = readline.createInterface({
      input: readStream,
    });

    var objs = [];

    // the 'line' event happens when the next line is ready.
    // the anonymous function is a callback, and its argument (line) will be
    // filled by the readline library.
    rl.on('line', function(line) {
      try { // JSON.parse is synchronous and can throw exceptions
        var obj = JSON.parse(line);
        objs.push(obj);
      } catch (parseError) {
        console.warn("%s. Line skipped: %s", parseError, line);
      }
    });

    // the 'close' event happens when the input stream ends
    rl.on('close', function() {
      callback(null, objs);
    });
  });
}

function main() {
  // load all users
  loadLinesAsObjs('flickr100k-users', function(err, users) {
    if (err) { return console.error(err); }

    // build a dictionary from userId to user objects, for quick lookup
    var userDict = {};
    users.forEach(function(user) { userDict[user.id] = user; });

    // then, load all photos
    loadLinesAsObjs('flickr100k-photos', function(err, photos) {
      if (err) { return console.error(err); }

      photos.forEach(function(photo) {
        if (photo.user.id in userDict) {
          // replace photo.user (which contains only user ID and nickname) with
          // the user object that may contain following users and groups:
          photo.user = userDict[photo.user.id];
        }
        console.log(JSON.stringify(photo));
      });
    });
  });
}

main();

