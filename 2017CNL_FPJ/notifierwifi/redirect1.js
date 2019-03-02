// dB, MHz -> meter
function ComputeDistance(signal_level_diff, freq)
{
    return Math.pow(10, 0.05 * signal_level_diff - 4.622) / freq
}

// @corridor
function MyComputeDistance(signal_level_diff, freq)
{
    return Math.pow(10, 0.05 * signal_level_diff + 2.447) / freq
}

// b11: redirect to the web page of AP with max signal level
// return ssid of closest AP
function Redirect1(networks)
{
	var min_distance = MyComputeDistance(-15-networks[0].signal_level, networks[0].frequency);
    //var min_distance = ComputeDistance(networks[0].signal_level - networks[0].transmit_signal_level, networks[0].frequency);
    var min_j = 0;
    for(var j=1; j<networks.length; j++){
        var distance = MyComputeDistance(-15-networks[j].signal_level, networks[j].frequency);
        //console.log(networks[index[j]].ssid, networks[index[j]].signal_level, networks[index[j]].frequency, distance)
        //var distance = ComputeDistance(networks[i].signal_level - networks[i].transmit_signal_level, networks[i].frequency);
        if(distance < min_distance){
            min_distance = distance;
            min_j = j;
        }
    }
    return networks[min_j].ssid;
}

var fs = require('fs');
var networks;

// assuming filename = './networks.json'
fs.readFile('./networks.json', 'utf8', function (err,data) {
  if (err) throw err;
  networks = JSON.parse(data);
});

var webs = {'7':'www.pcs.csie.ntu.edu.tw/course/cnl/2017/',
			'12':'www.csie.ntu.edu.tw/~htlin/',
			'13':'www.csie.ntu.edu.tw/~cjlin/' };

console.log(webs[Redirect1(networks)]);