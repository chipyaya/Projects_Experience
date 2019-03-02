var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var fs = require('fs');
var firebase = require('firebase');
var app = express();

var ref = new firebase('https://ntuaf-door.firebaseio.com/ratio5');
ref.authWithCustomToken('FdVNtgTiJwhnXYELrxW2auWwGRWopXCjWrPej7Gb');


app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res){
	res.render('index');
})

app.get('/winloo', function(req, res){
	fs.readFile('./ratio.txt', 'utf8', function(err,data){
		var win = parseInt(data);
		console.log('win = '+win);
		res.json({result: win});
	});
})

app.get('/ratio5', function(req, res){
	ref.once("value", function(snapshot) {
		  console.log(snapshot.val());
		  res.json({result: snapshot.val()});
	}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
	});

});


app.listen(3001, function () {
	console.log('Example app listening on port 3001!');
});
