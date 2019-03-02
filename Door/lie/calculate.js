var qs = [];
var ans = [];
var timerecord = [];
var pulserecord = [];

var scoretable = {
	2:[10,1,0],
	4:[10,10,10,0],
	5:[10,10,10,10,10,0],
	6:[10,1,0],
	7:[10,1,0],
	8:[10,1,0],
	9:[10,1,0],
	10:[10,1,0],
	11:[10,1,0],
	12:[10,1,0],
	14:[1,10,0],
	16:[10,1,0],
	20:[10,1,0],
	21:[10,1,0],
	22:[10,1,0],
	23:[1,10,0]
}

function liepanelty(qs,ans,timespend,pulse){
	var panel = 0;
	for(var i = 0; i < timespend.length; i++){
		var pulse_per_msec = pulse[i]/timespend[i];
		if(pulse_per_msec >= 80/6000)
			panel += scoretable[qs[i]][ans[i]];
	}
	console.log('panel',panel);
	return panel;
}

function calpulse(pulserecord){
	var pulse = [];

	for(var i = 0; i < pulserecord.length-1; i++)
		pulse[i] = pulserecord[i+1] - pulserecord[i];
	
	return pulse;
}

function caltimespend(timerecord){

	var time = [];

	for(var i = 0; i < timerecord.length-1; i++)
		time[i] = timerecord[i+1] - timerecord[i];

	return time;
}

function caltmean(qs,timespend){
	
	var tmean = 0;
	var record = 0;
	
	for(var i = 0; i < qs.length; i++){
		
		var q = qs[i];

		if(!(q in scoretable)){
			record ++;
			tmean += timespend[i];		
		}
	}
	tmean /= record
	return tmean;
}

var cal = function(qs,ans,timerecord,pulserecord){
	
	var timespend = caltimespend(timerecord);
	var pulse = calpulse(pulserecord);
	var tmean = caltmean(qs,timespend);
	
	var totalscore = 0;

	var record_0 = 0;
	
	for(var i = 0; i < qs.length; i++){
		
		var q = qs[i];
		var a = ans[i];
		
		if(q in scoretable){
			var score = scoretable[q][a];
			if(score == 0)
				record_0++;
			var adjust_score = score*(tmean/(score+tmean));
			totalscore += adjust_score;
		}
	}

	if(totalscore > 100)
		totalscore = 100;
	
	else if(totalscore == 0)
		totalscore = 50;
	
	else{
		totalscore = totalscore / (ans.length - record_0) * ans.length
		totalscore -= liepanelty(qs,ans,timespend,pulse);
	}

	var level = 5 - parseInt(totalscore/20);

	console.log('totalscore',totalscore);

	return level;
}

module.exports.qs = qs;
module.exports.ans = ans;
module.exports.timerecord = timerecord;
module.exports.pulserecord = pulserecord;
module.exports.cal = cal;
