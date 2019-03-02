var currentUser = "";
var receiver = "";
var userDoc = [];

module.exports = {
	setCurrentUser: function(username){currentUser = username;},
	getCurrentUser: function(){ return currentUser; },
	setReceiver: function(receivername){receiver = receivername; },
	getReceiver: function(){return receiver; },
};
