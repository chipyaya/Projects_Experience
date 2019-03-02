var express = require('express');
var fileUpload = require('express-fileupload');
//var user = require('./user');
var router = express.Router();
var cp = require('node-cp');
var async = require('async');

var currentUser;
var receiver;
var debugMsg = "";
var debugFile = "";
var searchRes = [];
//import {router, currentUser} from './register';

// show importantMsg and unreadMsg
router.get("/", function(req, res){
	currentUser = req.query.currentUser;
    var db = req.db;
	var userDoc, importantDoc, unreadDoc;
    var collection = db.get('usercollection');
    collection.find({},{},function(e,docs){
		userDoc = docs;
		collection = db.get('msgcollection');
			collection.find({"receiver": currentUser, "important": "on"},function(e,docs2){
					importantDoc = docs2;
					collection.find({"receiver": currentUser, "read": 0},function(e,docs3){
						unreadDoc = docs3;
						res.render('msg', { title: 'Messenger' , currentUser: currentUser, userDoc: userDoc, importantDoc: importantDoc, unreadDoc: unreadDoc, debugMsg:debugMsg});
                  debugMsg = "";
                  debugFile = "";
			});
		});
    });
});

router.post("/", function(req, res){
   receiver = req.body.receiver;
   res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
});

// search msg
function Item(req, delay){
    this.delay = delay;
	searchReq = req.body.searchReq;
	var db = req.db;
	var msgcollection = db.get('msgcollection');
    var usercollection = db.get('usercollection');
	var finish = 0;
	var usernameL = [];
	var msgContent;
	
    usercollection.find({},{},function(e,docs){
		var i;
		for(i = 0; i < Object.keys(docs).length; i++){
			usernameL.push(docs[i].username);
		}
		usernameL.forEach(function(username, i){
			msgcollection.find({"sender": username, "receiver": currentUser}, {}, function(err, docs2){
				for(j = 0; j < Object.keys(docs2).length; j++){
					msgContent = docs2[j].msgContent;
					if(docs2[j].msgContent.indexOf(searchReq) > -1) {
                  searchRes.push({sender: username, receiver: currentUser, content: msgContent});
					}
				}
			});
			msgcollection.find({"sender": currentUser, "receiver": username}, {}, function(err, docs3){
				for(j = 0; j < Object.keys(docs3).length; j++){
					msgContent = docs3[j].msgContent;
					if(docs3[j].msgContent.indexOf(searchReq) > -1) {
						searchRes.push({sender: currentUser, receiver: username, content: msgContent});
					}
				}
			});
		});
	});

}

function renderSearchRes(res){
	res.render("searchRes", {searchRes: searchRes});
}


router.post("/msgSearch", function(req, res){
	searchRes = []

	Item.prototype.someAsyncCall = function(callback){
		console.log('delay:', this.delay);
		setTimeout(function(){
			if(typeof callback === "function") callback();
		}, this.delay);
	};

	var items = [];
	items.push(new Item(req, 1000));

	async.each(items,
	  function(item, callback){
		item.someAsyncCall(function (){
		  callback();
		});
	  },
	  function(err){
		renderSearchRes(res);
	  }
	);
});

// go to next page and show history
router.get("/msgSend", function(req, res){
   currentUser = req.query.currentUser;
   receiver = req.query.receiver;
      
   var db = req.db;
   var usercollection = db.get('usercollection');
   var msgcollection = db.get('msgcollection');
   var filecollection = db.get('filecollection');
   usercollection.find({"username": receiver} , function(err, docs){
		if(Object.keys(docs).length == 0){
			console.log("no this account");
			debugMsg = "no this account";
			res.redirect("/msg?currentUser="+currentUser);
		}
		else{
         usercollection.find({"username": currentUser}, function(err, docs5){
            if(Object.keys(docs5).length != 1) console.log("there are some errors");
            msgcollection.find({"sender":receiver, "receiver":currentUser}, function(err, docs4){
               for(i = 0; i < Object.keys(docs4).length; i++){
                  msgcollection.update({_id: docs4[i]._id}, {$set: {read:1}});
               }
               
               msgcollection.find({$or:[{"sender":receiver, "receiver":currentUser}, {"sender":currentUser, "receiver": receiver}]}, function(err, docs2){
                  filecollection.find({$or:[{"sender":receiver, "receiver":currentUser}, {"sender":currentUser, "receiver": receiver}]}, function(err, docs3){
                     res.render('msgSend', {sender:currentUser, receiver:receiver, msgs:docs2, files:docs3, debugFile:debugFile, customizeMsg: docs5[0].customizeMsg});
                     debugFile = "";
                  });
                });  
             }); 
           }); 
         } 
   });
   //console.log(files.sendFile.sendFile.name);
});

//router.use("/msgSend/file", fileUpload());
router.use(fileUpload());

// send a msg
router.post("/msgSend/msgcontent", function(req, res){
   var db = req.db;
   currentUser = req.body.currentUser;
   receiver = req.body.receiver;
   var sendMsg;
   console.log("debug2");
   sendMsg = req.body.sendMsg;
   important = req.body.important;

   var msgcollection = db.get("msgcollection");
   msgcollection.insert({
      "sender" : currentUser,
      "receiver" : receiver,
      "msgContent" : sendMsg,
	  "read" : 0,
	  "important": important
       }, function(err, doc){
         res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
      });
});

// get uploaded file
router.post("/msgSend/file", function(req, res){
   var db = req.db;
   currentUser = req.body.currentUser;
   receiver = req.body.receiver;
   var sendFile;
   if(!req.files){
      debugFile = "you haven't sent any file";
      res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
   }  
   else if(req.files.sendFile.name.length == 0){
      console.log("no file actually!");
      debugFile = "you haven't sent any file";
      res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
   } 
   else{
      sendFile = req.files.sendFile;
      console.log(sendFile.name);
      sendFile.mv('./files/'+currentUser+"_"+receiver+"_"+sendFile.name, function(err){
         if(err){
            debugFile = err;
            res.status(500).redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
         }
         else{
            var filecollection = db.get('filecollection');
            filecollection.insert({
               "sender" : currentUser,
               "receiver" : receiver,
               "filename" : currentUser+"_"+receiver+"_"+sendFile.name
            }, function (err, doc) {
				if (err) {
				   // If it failed, return error
				   debugFile = "there's some problems with db.";
				   res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
				}
				else {
				   // And forward to success page
				   debugFile = "success send a file";
				   res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
				}
			});

         }
      });
   }
});
router.get("/msgSend/:name", function(req, res, next){
   var options = {
      root: './files/',
      headers:{
         'x-timestamp':Date.now(),
         'x-sent':true
      }
   };
   var filename = req.params.name;
   res.sendFile(filename, options, function(err){
      if(err){
         console.log(err);
         res.status(err.status).end();
      }
      else{
         console.log("file sent success");
      }
   });
});

router.post("/msgSend/customizeSet", function(req, res){
   var customizeMsg = req.body.customizeMsg;
   currentUser = req.body.currentUser;
   var db = req.db;
   var usercollection = db.get("usercollection");
   usercollection.find({"username":currentUser}, function(err, doc){
      if(err){
         console.log(err);
      }
      else if(Object.keys(doc).length != 1){
         console.log("there are some errors");
      }
      else{
         usercollection.update({username: currentUser}, {$set: {customizeMsg: customizeMsg}});
         console.log("update customizeMsg");
         res.send("success");
      }
   });
});

router.post("/msgSend/customizeSend", function(req, res){
   var customizeMsg = req.body.customizeMsg;
   console.log("get customizeMsg:" + customizeMsg);
   currentUser = req.body.sender;
   receiver = req.body.receiver;
   var db = req.db;
   var msgcollection = db.get("msgcollection");
   msgcollection.insert({
      "sender" : currentUser,
      "receiver" : receiver,
      "msgContent" : customizeMsg,
	  "read" : 0,
	  "important": 0
       }, function(err, doc){
          if(err) console.log(err);
          res.send("success");
          //res.redirect("/msg/msgSend?currentUser="+currentUser+"&receiver="+receiver);
      });

});

module.exports = router; 
