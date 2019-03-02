var wifi = require('node-wifi');
var func = require('./redirect');
var func2 = require('./savepoint.js')
 
wifi.init({
    iface : null 
});
 
var websites = {'7': 'google.com.tw', '12': 'www.ntu.edu.tw', '13': 'mrtg.csie.ntu.edu.tw'};
	
/*
const readline = require('readline');
if(readline[0] == 's'){
    console.log(readline);
    func2.saveCookies('0', newNetworks, 'www.google.com');
}
else if(readline[0] == 'g'){
    console.log(readline);
    console.log(getWebsiteBySavePoint(newNetworks));
}
*/
//func2.saveCookies('0', newNetworks, 'www.google.com');
//console.log(func2.getWebsiteBySavePoint(newNetworks));

var readline = require('readline');
var log = console.log;

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
var count=0;
var infiniteReadline = function () {
    rl.question('Command: ', function (input) {
        if(input[0] == 's'){
            console.log(input);
            wifi.scan(
                function(err, networks) {
                    if (err) {
                        console.log(err);
                    } 
                    else {
                        newNetworks = [];
                        for (var i = 0; i < networks.length; i++){
                            if(networks[i].ssid == '7' || networks[i].ssid == '12' || networks[i].ssid == '13'){
                                newNetworks.push(networks[i]);
                            }
                        }
                        newNetworks.sort(
                            function(a, b){
                              return parseInt(a.ssid) > parseInt(b.ssid);
                            }
                        );
                        /*
                        for (var i = 0; i < newNetworks.length; i++){
                            console.log(newNetworks[i].ssid, newNetworks[i].frequency, newNetworks[i].signal_level)
                        }
                        */
                        func2.saveCookies(count, newNetworks, count);
                    }
                }
            );	
            count++;
        }
        else if(input[0] == 'g'){
            console.log(input);
            wifi.scan(
                function(err, networks) {
                    if (err) {
                        console.log(err);
                    } 
                    else {
                        newNetworks = [];
                        for (var i = 0; i < networks.length; i++){
                            if(networks[i].ssid == '7' || networks[i].ssid == '12' || networks[i].ssid == '13'){
                                newNetworks.push(networks[i]);
                            }
                        }
                        newNetworks.sort(
                            function(a, b){
                              return parseInt(a.ssid) > parseInt(b.ssid);
                           }
                        );
                        /*
                        for (var i = 0; i < newNetworks.length; i++){
                            console.log(newNetworks[i].ssid, newNetworks[i].frequency, newNetworks[i].signal_level)
                        }
                        */
                        console.log(func2.getWebsiteBySavePoint(newNetworks));
                    }
                }
            );
        }
        infiniteReadline(); //Calling this function again to ask new question
    });
};

infiniteReadline(); //we have to actually start our recursion somehow

