var async = require('async')
var wifi = require('node-wifi');
var sleep = require('sleep');
var func = require('./redirect');

var ssids_fix = ['7', '12', '13']
var freqs_fix = [2437, 2437, 2412]
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

for (var i = 0; i < ssids_fix.length; i++){
    ssid2website[ssids_fix[i]] = websites1[i]
    signal_levels.push([])
}

var sampleN = 1
var array = new Array(sampleN-1)

for (var i = 0; i < array.length; i++){
    array[i] = i+1
}

function doSomething(newNetworks, callback){
    return callback(ssid2website[func.Redirect1(newNetworks)]);
}

function foo(url){
    return url
}

function median(a){
    a.sort()
    return a[parseInt((sampleN+1)/2)]
}


wifi.init({
    iface : null // network interface, choose a random wifi interface if set to null 
});
 
function scan(case_num){
    async.waterfall([
        function(callback){
            wifi.scan(function(err, networks) {
                console.log(networks)
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
        //console.log('Median:', newNetworks);

        if(case_num == 1){
            if(newNetworks.length > 0){
                //doSomething(newNetworks, foo)
                //return ssid2website[func.Redirect1(newNetworks)]
                //var ssid_ret = func.Redirect1(newNetworks)
                //console.log('Redirect1:', ssid_ret, ssid2website[ssid_ret]);
                //open(ssid2website[ssid_ret], 'google-chrome');
                //return ssid2website[ssid_ret]
                url = ssid2website[func.Redirect1(newNetworks)]

            }
            else{
                console.log('Cannot detect enough APs (at least 1 for case 1)')
            }
        }
        else if(case_num == 2 ){
            if(newNetworks.length == 3){
                var ssid_ret2 = func.Redirect2(newNetworks, [0.6 * 10, 0.6 * Math.pow(1+16, 0.5), 0.6 * Math.pow(81+16, 0.5)]);
                console.log('Redirect2:', ssid_ret2, websites2[ssid_ret2]);
                return websites2[ssid_ret2]
                //open(websites2[ssid_ret2], 'google-chrome');
            }
            else{
                console.log('Cannot detect enough APs (at least 3 for case 2)')
            }
        }
        else if(case_num == 3){
            return newNetworks
        }
    });
}


exports.scan = scan
