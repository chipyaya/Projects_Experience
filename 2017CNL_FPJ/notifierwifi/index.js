/**
 * Usage for case 1: node index.js 1
 * Usage for case 2: node index.js 2
 * Usage for case 3: node index.js 3
 * 
 * Before executing:
 *     Please set 
 *     (1) ssids_fix[] and its corresponding freqs_fix[]
 *     (2) websites1[] and websites2[] that you want to direct to
 *     
**/

var async = require('async')
var wifi = require('node-wifi');
var open = require('open');
var sleep = require('sleep');
var func = require('./redirect');

var ssids_fix = ['7', '12', '13']
//var ssids_fix = ['ntu_peap', 'NTU', 'ntu_peap']
var freqs_fix = [2412, 2412, 2437]
var websites1 = ['google.com.tw', 'www.ntu.edu.tw', 'mrtg.csie.ntu.edu.tw']
var websites2 = ['www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab1_Firewall_NAT(concept).pdf',
                'www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab1_Firewall_NAT(exeriment).pdf',
                'www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab2_concept.pdf',
                'www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab2_experiment.pdf',
                'www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab3_IPv6_Mobility(concept).pdf',
                'www.pcs.csie.ntu.edu.tw/views/courses/cnl/2017/2017_Lab3_IPv6_Mobility(experiment).pdf'];

var ssid2website = {}
var signal_levels = []
//var sleep_seconds = 1

var myArgs = process.argv.slice(2);
var case_num = myArgs[0]
//console.log(case_num);
//if(myArgs.length != 1 || !(case_num == 1 || case_num == 2 || case_num == 3)) {
if(!(case_num == 1 || case_num == 2 || case_num == 3)) {
    console.log('Usage:\tnode index.js [case]\n\t[case] should be 1 or 2 or 3\n')
    throw new Error('Wrong arguments')
}

//console.log('case:', case_num);

for (var i = 0; i < ssids_fix.length; i++){
    ssid2website[ssids_fix[i]] = websites1[i]
    signal_levels.push([])
}

var sampleN = 5
var array = new Array(sampleN-1)

for (var i = 0; i < array.length; i++){
    array[i] = i+1
}

function median(a){
    a.sort()
    //console.log(a, a[parseInt((sampleN)/2)])
    //console.log(a[parseInt((sampleN)/2)])
    return a[parseInt((sampleN)/2)]
}


wifi.init({
    iface : null // network interface, choose a random wifi interface if set to null 
});
 
async.waterfall([
    function(callback){
        wifi.scan(function(err, networks) {
            //console.log(networks)
            var newNetworks = []
            if (err) {
                console.log(err);
            } else {
                for (var i = 0; i < networks.length; i++){
                    for (var j = 0; j < ssids_fix.length; j++){
                        if((networks[i].ssid == ssids_fix[j]) && (networks[i].frequency == freqs_fix[j])){
                        //if(networks[i].ssid == ssids_fix[j]){
                            signal_levels[j].push(networks[i].signal_level)
                            newNetworks.push(networks[i])
                        }
                    }
                }
                newNetworks.sort(function(a, b){
                    return parseInt(a.ssid) > parseInt(b.ssid)
                })
            }
            //console.log('init:', newNetworks)
            callback(null, newNetworks);
        })
    },
    function(newNetworks, callback){
        async.everySeries(array, function(c, callback){
            //sleep.sleep(sleep_seconds)      // sleep sleep_seconds seconds
            wifi.scan(function(err, networks) {
                if (err) {
                    console.log(err);
                } else {
                    for (var i = 0; i < networks.length; i++){
                        for (var j = 0; j < ssids_fix.length; j++){
                            if((networks[i].ssid == ssids_fix[j]) && (networks[i].frequency == freqs_fix[j])){
                            //if(networks[i].ssid == ssids_fix[j]){
                                signal_levels[j].push(networks[i].signal_level)
                            }
                        }
                    }
                    callback(null, !err);
                }
            })

        }, function (err, result) {
            callback(null, newNetworks)
        });
    },
], function (err, newNetworks) {
    for (var i = 0; i < newNetworks.length; i++){
        newNetworks[i].signal_level = median(signal_levels[i])
    }
    if(case_num == 1){
	    //console.log(newNetworks)
        if(newNetworks.length > 0){
            var ssid_ret = func.Redirect1(newNetworks)
            console.log('Redirect1:', ssid_ret, ssid2website[ssid_ret]);
            open(ssid2website[ssid_ret], 'google-chrome');
        }
        else{
            console.log('Cannot detect enough APs (at least 1 for case 1)')
        }
    }
    else if(case_num == 2 ){
        if(newNetworks.length == 3){
	    var x = myArgs[1];
            var y = myArgs[2];
    	    console.log(x,y,newNetworks[0].signal_level,newNetworks[1].signal_level,newNetworks[2].signal_level);
            var ssid_ret2 = func.Redirect2(newNetworks, [-0.9,5.4 , 4.2]);
	    //console.log('Redirect2:', ssid_ret2, websites2[ssid_ret2]);
            open(websites2[ssid_ret2], 'google-chrome');
        }
        else{
            console.log('Cannot detect enough APs (at least 3 for case 2)')
        }
    }
    else if(case_num == 3 ){

    }
});
