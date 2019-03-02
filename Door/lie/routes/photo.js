var express = require('express'); var router = express.Router(); var https = require('https');
var bodyParser = require('body-parser');
var FB = require('fb');
var fs = require('fs');
var request = require('request');
var imgur = require('imgur');
var qr = require('qr-image');
var FormData = require('form-data');
var exec_cmd = require('child_process').exec;
var cal = require('../calculate.js');
var im = require('imagemagick');
var firebase = require('firebase');

var ref = new firebase('https://ntuaf-door.firebaseio.com/ratio5');
ref.authWithCustomToken('FdVNtgTiJwhnXYELrxW2auWwGRWopXCjWrPej7Gb');

router.get('/', function(req, res){
	res.render('index');
})

var lastpulse;
var photourl;

fs.readFile('hardware/heartBeat/heartBeat.txt', 'utf8', function(err,data){
	lastpulse = parseInt(data);
});

// make it start automatically if it can detect pulse
router.get('/detectstart', function(req, res){
	fs.readFile('hardware/heartBeat/heartBeat.txt', 'utf8', function(err,data){
		console.log(parseInt(data),lastpulse)
			if(parseInt(data) > lastpulse)
				res.json({result:1});
			else
				res.json({result:0});
	});
})

// clean data before begining
router.get('/clean', function(req, res){
	//clean calculate pulse data
	cal.qs = [];
	cal.ans = [];
	cal.timerecord = [];
	cal.pulserecord = [];
	res.end();

	//clean all img under kinect_people folder
	var dirPath = './kinect_code/NTUAF-Recognize/NTUAF-Recognize/images/';
	var files = fs.readdirSync(dirPath); 
	if(files.length > 0){
		for(var i = 0; i < files.length; i++){
			var filePath = dirPath + '/' + files[i];
			if(fs.statSync(filePath).isFile())
				fs.unlinkSync(filePath);
		}
	}
})

router.get('/questions', function(req, res){
	cal.qs = [];
	cal.ans = [];
	cal.timerecord = [];
	cal.pulserecord = [];
	var d = new Date();
	cal.timerecord.push(d.getTime());
	// Read pulserecord number from pulserecord.txt
	fs.readFile('hardware/heartBeat/heartBeat.txt', 'utf8', function(err,data){
		cal.pulserecord.push(parseInt(data));
	});
	res.render('questions');
});

router.post('/Q', function(req, res){
	console.log(req.body.qnum, req.body.ans);
	// Read pulserecord number from pulserecord.txt
	fs.readFile('hardware/heartBeat/heartBeat.txt', 'utf8', function(err,data){
		if (err) throw err;
		//recode time and pulserecord number per question
		var d = new Date();
		cal.qs.push(req.body.qnum);
		cal.ans.push(req.body.ans);
		cal.timerecord.push(d.getTime());
		cal.pulserecord.push(parseInt(data));
		console.log(cal.timerecord);
	});

	res.end();
})

router.get('/detectfinish', function(req, res){
	fs.readFile('kinect_code/finish.txt', 'utf8', function(err,data){
		if(parseInt(data) == 1)
			res.json({result:1});
		else
			res.json({result:0});
	});
})

router.get('/gotoshoot', function(req,res){
	// set finish.txt to 0
	fs.writeFile('kinect_code/finish.txt', '0', 'utf8');
	res.render('gotoshoot');
});

router.get('/loading', function(req,res){
	res.render('loading');
	
});

router.get('/uploadtoimgur', function(req, res){		//call by pressing the button in question.jade
	lastpulse = cal.pulserecord[cal.pulserecord.length-1];
	var level = cal.cal(cal.qs,cal.ans,cal.timerecord,cal.pulserecord);	//depends on %	//depends on %
	fs.readFile('kinect_code/coordinate.txt', 'utf8', function(err,data){
		var sh = 'processImg.bat';
		var level = cal.cal(cal.qs,cal.ans,cal.timerecord,cal.pulserecord);	//depends on %	//depends on %
	
		fbase.once("value", function(obj) {
			console.log('key','l'+String(level), 'val', obj.val()['l'+String(level)])
			var newobj = {};
			var key = 'l'+String(level);		
			newobj[key] = obj.val()['l'+String(level)]+1;
			fbase.update(newobj);


			
		}, function (errorObject) {
  			console.log("The read failed: " + errorObject.code);
		});	
		var strarr = data.split("\r\n");
		var filename = parseInt(strarr[0]);
		var centerX = parseInt(strarr[1]);
		var centerY = parseInt(strarr[2]);
		var str = [
			sh,
			level.toString(),
			filename.toString(),
			centerX.toString(),
			centerY.toString(),
		]
		cmd = str.join(' ');
		console.log(cmd);

		console.log('before exec');
		//processing the image
 
		exec_cmd(cmd, function(err, data){	

		console.log(err);
		console.log(data.toString());                       
		console.log('after exec');
		var albumId = 'fGZi1';
		imgur.uploadFile('public/img/composite.png', albumId)	//upload to imgur
			.then(function (json) {
				photourl = json.data.link;
				console.log(photourl);
				//res.redirect('/share');
				res.json(json);
			})
			.catch(function (err) {
				console.error(err.message);
			});

		});
	});
});															// return to sharephoto.js

router.get('/share', function(req, res){			//call by pressing the button in questions.jade
	res.render('sharephoto');
});

router.get('/makeqrcode', function(req,res){		//call by pressing the button in sharephoto.jade
	var qrcode = qr.image(photourl, { type: 'svg' });	
	res.type('svg');
	qrcode.pipe(res);
});


router.post('/uploadtofb', function(req, res){		//call by sharephoto.js

	var ACCESS_TOKEN = req.body.token;
	var message = req.body.message;

	var form = new FormData(); //Create multipart form
	form.append('file', fs.createReadStream('public/img/composite.png')); //Put file
	form.append('message', message); //Put message

	var options = {
		method: 'post',
		host: 'graph.facebook.com',
		path: '/me/photos?access_token='+ACCESS_TOKEN,
		headers: form.getHeaders()
	}

	var request = https.request(options, function (res){
		console.log(res);
	});

	form.pipe(request);
	res.end();
})

module.exports = router;
