var express = require('express');
var router = express.Router();
//var user = require('./user'); 
var msg = require('./msg');
router.use('/msg', msg);

var crypto = require('crypto'),
    algorithm = 'aes-256-ctr',
    password = 'd6F3EfeqQ';

function encrypt(text){
	var cipher = crypto.createCipher(algorithm,password)
	var crypted = cipher.update(text,'utf8','hex')
	crypted += cipher.final('hex');
	return crypted;
}
 
/* Login */
router.post('/login', function (req, res) {
    var db = req.db;
    var userName = req.body.username;
    var userPasswd= req.body.userpasswd;
    var collection = db.get('usercollection');

	// UserName or Passwd is blank
	if(userName.length == 0 || userPasswd.length == 0){
		res.render('index', {
			title: 'Welcome to Messenger',
			loginStatus : "Please input your account and password"
		});
	}
	// UserName and Passwd isn't blank
	else{
		collection.find({"username": userName}, function (err, docs){
			// Username exists
			if(Object.keys(docs).length > 0){
				collection.find({"username": userName, "userpasswd": encrypt(userPasswd)}, function (err, docs2){
					// Wrong userPasswd
					if(Object.keys(docs2).length == 0){
						res.render('index', {
							title: 'Welcome to Messenger',
							loginStatus : "Wrong password"
						});
					}
					// Correct userPasswd
					else{
						res.redirect("/msg?currentUser="+userName);
					}
				});
			}

			// Username doesn't exists
			else{
				res.render('index', {
					title: 'Welcome to Messenger',
					loginStatus : "Wrong userName"
				});
			}
		});
	}
});

/* Signup */
router.post('/signup', function(req, res) {
    var db = req.db;
    var userName = req.body.username;
    var userPasswd= req.body.userpasswd;
    var collection = db.get('usercollection');

	if(userName.length == 0 || userPasswd.length == 0){
		res.render('index', {
			title: 'Welcome to Messenger',
			signupStatus : "Account and Password can't be blank" 
		});
	}
	else{
		collection.find({"username": userName}, function (err, docs){
			// The username has already been used
			if(Object.keys(docs).length > 0){
				res.render('index', {
					title: 'Welcome to Messenger',
					signupStatus : "Username exists. Try another one" 
				});
			}
			else{
				// The username hasn't been used, submit to the DB
				collection.insert({
					"username" : userName,
					"userpasswd" : encrypt(userPasswd),
               "customizeMsg" : ""
				}, function (err, doc) {
					if (err) {
						res.send("There was a problem adding the information to the database.");
					}
					else {
						//forward to success page
						res.redirect("/msg?currentUser="+userName);
					}
				});
			}
		});
	}
});

/* changepasswd*/
router.post('/changepasswd', function(req, res) {
    var db = req.db;
    var userName = req.body.username;
    var oldPasswd= req.body.oldpasswd;
    var newPasswd= req.body.newpasswd;
    var collection = db.get('usercollection');

	// UserName or Passwd is blank
	if(userName.length == 0 || oldPasswd.length == 0 || newPasswd.length == 0){
		res.render('index', {
			title: 'Welcome to Messenger',
			changepasswdStatus : "Please input your account, old password, and new password."
		});
	}
	collection.find({"username": userName}, function (err, docs){
		// Username exists
		if(Object.keys(docs).length > 0){
			collection.find({"username": userName, "userpasswd": encrypt(oldPasswd)}, function (err, docs2){
				// Wrong oldPasswd
				if(Object.keys(docs2).length == 0){
					res.render('index', {
						title: 'Welcome to Messenger',
						changepasswdStatus : "Wrong old password"
					});
				}
				// Correct oldPasswd
				else{
					// Change password
					collection.update({_id: docs2[0]._id}, {$set: {userpasswd: encrypt(newPasswd)}});
					res.render('index', {
						title: 'Welcome to Messenger',
						changepasswdStatus : "Password has been changed successfully"
					});
					
				}
			});
		}

		// Username doesn't exists
		else{
			res.render('index', {
				title: 'Welcome to Messenger',
				changepasswdStatus : "Wrong userName"
			});
		}
	});

});

module.exports = router;
