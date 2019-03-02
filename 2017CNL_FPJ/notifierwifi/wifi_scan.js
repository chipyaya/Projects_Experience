var wifi = require('node-wifi');
var func = require('./redirect');
var fs = require('fs');

wifi.init({
    iface : null // network interface, choose a random wifi interface if set to null 
});

wifi.scan(function(err, networks) {
    if (err) {
        console.log(err);
    } else {
        newNetworks = []
        for (var i = 0; i < networks.length; i++){
            if(networks[i].ssid == '7' || networks[i].ssid == '12' || networks[i].ssid == '13'){
                newNetworks.push(networks[i]);
            }
        }
        /*
        newNetworks.sort(function(a, b){
            return parseInt(a.ssid) > parseInt(b.ssid);
        })
        */
        var json = JSON.stringify(newNetworks);
        console.log(json);
        /*
        for (var i = 0; i < newNetworks.length; i++){
            console.log(newNetworks[i].ssid, newNetworks[i].signal_level);
        }
        var ssid_ret = func.Redirect1(newNetworks)
        console.log(ssid_ret)
        func.Redirect2(newNetworks, [4.8, 4.817, 3.94]);
        */
    }
});
