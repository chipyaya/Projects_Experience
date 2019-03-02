var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
var fs = require('fs');

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('index.ejs');
});

var arg = "";

router.post('/transfer_input', function(req, res){
	var stateN = parseInt(req.body.stateN);
	var inputN = parseInt(req.body.inputN);
	arg = "";
	arg += req.body.stateN+" ";
	arg += req.body.inputN+" ";
	var i;
	var sum = stateN+inputN;
	for(i = 0; i < stateN; i++){
		arg += req.body.type[i]+" ";
	}
	for(i = 0; i < parseInt(Math.pow(2, sum)); i++){
		arg += i+" ";
		arg += req.body.newState[i]+" ";
		arg += req.body.output[i]+" ";
	}
	res.end();
});

router.get('/makeCircuit', function(req, res){
	// execute forward_alg
	console.log('arg of sdt', arg);
	var child = exec('./sdt '+arg, (error, stdout, stderr) => {
		if (error) {
			throw error;
		}
		console.log(stdout);
		res.end(stdout);
	});
});

module.exports = router;
