var express = require('express');
var router = express.Router();
var exec = require('child_process').execFile;
var exec_command = require('child_process').exec;
var fs = require("fs");

router.get('/tv', function(req, res){
	res.render('tv');
})

router.post('/ratio', function(req, res){
	fs.readFile('ratio.txt', 'utf8', function(err,data){
		var win_ratio = parseInt(data);
		res.json({ ratio: win_ratio});
	})
})

router.post('/openosk', function(req, res){
	exec_command("osk", function(error, stdout, stderr) {});
});

module.exports = router;
