var express = require('express');
var router = express.Router();

router.get('/cleanDB', function(req, res) {
    var db = req.db;
	db.collection("usercollection").remove({},function(err,numberRemoved){
		console.log("inside remove call back" + numberRemoved);
	});
	db.collection("msgcollection").remove({},function(err,numberRemoved){
		console.log("inside remove call back" + numberRemoved);
	});
	db.collection("filecollection").remove({},function(err,numberRemoved){
		console.log("inside remove call back" + numberRemoved);
	});
	res.redirect("/");
});

router.get('/showDB', function(req, res) {
    var db = req.db;
    var collection = db.get('usercollection');
    collection.find({},{},function(e,docs){
		var collection = db.get('msgcollection');
		collection.find({},{},function(e,docs2){
			res.render('showDB', {
				"userlist" : docs,
				"allMsg": docs2
			});
		});
    });
});
module.exports = router;
