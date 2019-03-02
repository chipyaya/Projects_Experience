var savePoints = {};

//class SavePoint
var SavePoint = function(network){
	var self = this;
	self.wifiAmps = {};
	self.website = "";
	for(var i=0;i<network.length;i++){
		self.wifiAmps[network[i].ssid] = network[i].signal_level;
	}
	self.bind = function(website){
		self.website = website;
	}
}
//inner product
SavePoint.compare = function(sp1, sp2){
	var dot = 0;
	var allkeys = new Set();
	for(var key in sp1.wifiAmps){
		allkeys.add(key);
	}
	for(var key in sp2.wifiAmps){
		allkeys.add(key);
	}
	for(let key of allkeys){
		var amp1 = 0, amp2 = 0;
		if(sp1.wifiAmps[key]!=null){
			amp1 = Math.pow(10, sp1.wifiAmps[key]/10);
		}
		if(sp2.wifiAmps[key]!=null){
			amp2 = Math.pow(10, sp1.wifiAmps[key]/10);
		}
		dot += (amp1-amp2)*(amp1-amp2);
	}
	return dot;
}

function getWebsiteBySavePoint(network){
	var savePoint = new SavePoint(network);
	console.log("savePoints = ",savePoints);
	
	console.log("savePoints.length = ",savePoints.length);
	if(savePoints.length == undefined){
		console.log("savePoints.length = ",savePoints.length);
		return null;
	}
	//find the one that matches
	var min = 1000000;
	var minSavePoint = "";
	for(var name in savePoints){
		console.log("name = ",name);
		var dot = SavePoint.compare(savePoints[name], savePoint);
		if(dot < min){
			min = dot;
			minSavePoint = name;
		}
	}
	console.log("minSavePoint = ",minSavePoint);
	return savePoints[minSavePoint].website;
}

function saveCookies(name, network, website){
	var savePoint = new SavePoint(network);
	savePoint.bind(website);
	savePoints[name] = savePoint;
	var data = JSON.stringify(savePoints);
	var expires = new Date();
	expires.setTime(expires.getTime() + 10*365*24*60*60*1000);
	document.cookie = "savePointData=" + data + "; expires="+expires.toUTCString()+";";
}

function loadCookies(){
	var sp = {};
	var cookies = document.cookie.split(";");
	for(var key in cookies){
		var cookie = cookies[key].split("=");
		if(cookie[0]=="savePointData"){
			try{
				sp = JSON.parse(unescape(cookie[1]));
			}
			catch(e){
				alert(e);
			}
		}
	}
	savePoints = sp;
}

exports.SavePoint = SavePoint;
exports.savePoints = savePoints;
exports.getWebsiteBySavePoint = getWebsiteBySavePoint;
exports.saveCookies = saveCookies;
