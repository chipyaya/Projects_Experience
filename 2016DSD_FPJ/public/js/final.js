var inputN, stateN, sumN;
function makeCircuit(){
	var type = [];
	var newState = [];
	var output = [];
	var i, j;
	for(i = 1; i <= stateN; i++){
		type.push($('input[name=type_Q'+i+']:checked').val());
	}
	for(i = 0; i < Math.pow(2, stateN+inputN); i++){
		var bin = "";
		for(j = 0; j < stateN; j++){
			bin += $('input[name='+i+'_'+j+']').val();
		}
		newState.push(parseInt(bin, 2));
		output.push(parseInt($('input[name='+i+'_'+stateN+']').val()));

	}

	//console.log(type, newState, output);
	var newState_str = "";
	var output_str = "";
	var type_str = "";
	for(i = 0; i < parseInt(Math.pow(2, stateN+inputN)); i++){
		newState_str += newState[i];
		output_str+= output[i];
		type_str+= type[i];
	}
	$.post('/transfer_input', {stateN: stateN, inputN: inputN, type: type_str, newState: newState_str, output: output_str}, function(data){
		$.get('/makeCircuit',function(data){
			var arg = data.split('\n');
			console.log(arg);
			doCanvas(arg);
		});
	});

}

function remove(id) {
	var elem = document.getElementById(id);
	elem.parentNode.removeChild(elem);
	return false;
}

function createInput(){
	inputN = parseInt($('input[name="inputN"]').val());
	stateN = parseInt($('input[name="stateN"]').val());
	sumN = inputN + stateN;
	createInputType(stateN);
	createInputTable(stateN, inputN);
	createButton();
	remove("myfieldset");

}

function createButton(){
	$("<br><button onClick='makeCircuit()'>Design Circuit</button>").insertAfter("#myTable");
}

function createInputType(){

	var i, j;

	for(i = stateN; i > 0; i--){
		$( "<form>Type of FF for Q"+i+":"+"<input type='radio' name='type_Q"+i+"' value='D' checked> D <input type='radio' name='type_Q"+i+"' value='T'> T <input type='radio' name='type_Q"+i+"' value='J'> JK <input type='radio' name='type_Q"+i+"' value='R'> RS Flip Flop</form><br>").insertAfter( "#pp" );
	}

}

function createInputTable(){
	var rowN = Math.pow(2, sumN);
	var table = document.getElementById("myTable");
	var header = table.createTHead();
	var row;  
	var cell;
	var i, j;


	//tbody
	for(i = 0; i < rowN; i++){
		//tr
		bin = i.toString(2);
		row = table.insertRow(table.rows.length);
		for(j = 0; j < sumN; j++){
			//td
			if(j < bin.length){
				cell = row.insertCell(table.rows[i].cells.length);		//insert from back
				cell.innerHTML = bin[j];
			}
			else{			//add 0 to the front
				cell = row.insertCell(0);
				cell.innerHTML = '0';
			}
		}
		for(j = 0; j < stateN+1; j++){
			cell = row.insertCell(table.rows[i].cells.length);		//insert from front
			cell.innerHTML = "<input name='"+i+"_"+j+"' type='number' value='0' min='0' max='1'>";
			//document.body.appendChild(p);

		}
	}

	//thead
	row = header.insertRow(0);
	for(j = 1; j <= stateN; j++){
		cell = row.insertCell(table.rows[0].cells.length);	//insert from back
		cell.innerHTML = 'Q'+j;
	}
	for(j = 1; j <= inputN; j++){
		cell = row.insertCell(table.rows[0].cells.length);	//insert from back
		cell.innerHTML = 'X'+j;
	}
	for(j = 1; j <= stateN; j++){
		cell = row.insertCell(table.rows[0].cells.length);	//insert from back
		cell.innerHTML = 'Q'+j+'+';
	}
	cell = row.insertCell(table.rows[0].cells.length);	//insert from back
	cell.innerHTML = 'Z';
}

function doCanvas(arg) {
	// Obtain a reference to the canvas element using its id.
	var htmlCanvas = document.getElementById('c'),

		// Obtain a graphics ctx on the  canvas element for drawing.
		ctx = htmlCanvas.getContext('2d');
	fitToContainer(htmlCanvas);

	// Start listening to resize events and draw canvas.
	initialize();

	function fitToContainer(canvas){
		canvas.style.width='100%';
		canvas.style.height='100%';
		canvas.width  = canvas.offsetWidth;
		canvas.height = canvas.offsetHeight;
	}

	function initialize() {
		// Register an event listener to call the resizeCanvas() function each time 
		// the window is resized.
		window.addEventListener('resize', resizeCanvas, false);

		// Draw canvas for the first time.
		resizeCanvas();
	}

	// Display custom canvas.
	function redraw() {
		//#input, #FF, type of FF-> 1:D 2:T 3:JK 4:SR
		//J1=120 211 -> y2 * x' + y1 * x
		//K1=212 
		//J2=210 
		//K2=002 110

		//arg = [ "2", "1", "101", "JK", "211", "202221", "D", "200012" ];
		stateN = parseInt(arg[0]);
		inputN = parseInt(arg[1]);
		var FF_type = [];
		var i;
		var tmp = 3;
		var exp = [];
		var output_exp = arg[2];

		for(i = 0; i < stateN; i++){
			var type_int;
			if(arg[tmp] == "D"){
				type_int = 1;
			}else if(arg[tmp] == "T"){
				type_int = 2;
			}else if(arg[tmp] == "JK"){
				type_int = 3;
			}else if(arg[tmp] == "RS"){
				type_int = 4;
			}
			FF_type.push(type_int);
			if(type_int <= 2){
				exp.push(arg[tmp+1]);
				tmp += 2;
			}else{
				exp.push(arg[tmp+1]);
				exp.push(arg[tmp+2]);
				tmp += 3;
			}
		}
		console.log(exp, FF_type);

		var web_h = $(document).height();
		var web_w = $(document).width();
		var FF_x = web_w-500;
		var i;

		ctx.scale(1/1.8, 1/1.8);

		leftLine();
		designOutput(output_exp);
		rightLine();

		var tmp2 = 0;
		for(i = 0; i < FF_type.length; i++){
			if(stateN == 1){
				FF(FF_type[i], FF_x, web_h, 150, 150);
			}
			else if(stateN <= 2){
				FF(FF_type[i], FF_x, ((i+1)/(stateN+1))*(web_h*2), 150, 150);
			}
			else if(stateN >= 3){
				FF(FF_type[i], FF_x, 300+(i/(stateN-1))*((web_h-100)*1.8), 150, 150);
			}

			if(FF_type[i] <= 2){
				link(i, -1, exp[tmp2]);
				tmp2++;
			}

			else if(FF_type[i] >= 3){
				link(i, -1, exp[tmp2]);
				link(i, 1, exp[tmp2+1]);
				tmp2 += 2;
			}
		}

	}

	// Runs each time the DOM window resize event fires.
	// Resets the canvas dimensions to match window, then draws the canvas accordingly.
	function resizeCanvas() {
		htmlCanvas.width = window.innerWidth;
		htmlCanvas.height = 2*window.innerHeight;
		redraw();
	}

	function link(FF_i, u_d, data){
		//J1=120 211 -> y1 * x' + y2 * x
		var i, j;
		var str = [];
		for(i = 0; i < data.length/sumN; i++){
			var tmp_str = "";
			for(j = 0; j < sumN; j++){
				tmp_str += data[i*sumN+j];
			}
			str.push(tmp_str);
		}   
		console.log(data, str);
		var web_h = $(document).height();
		var web_w = $(document).width();
		var FF_x = web_w-500;
		var FF_y; 
		if(stateN == 1){
			FF_y = web_h;
		}
		else if(stateN == 2){
			FF_y = ((FF_i+1)/(stateN+1))*(web_h*2);
		}
		else if(stateN >= 3){
			FF_y = 300+(FF_i/(stateN-1))*((web_h-100)*1.8);
		}
		var and_w = 50;
		var and_h = 50*(times/2);
		var hh = [];
		var and_x;
		for(i = 0; i < str.length; i++){
			var times = 0;
			var move_y;
			if(u_d == -1){
				move_y = -170+150*i;
				and_x = 300;
			}else if(u_d == 1){
				move_y = 120+150*i;
				and_x = 650;
			}
			for(j = 0; j < sumN; j++){
				if(parseInt(str[i][j]) != 2){
					var move_x = (parseInt(str[i][j]) == 1)? 0:1;
					var unit_l = 20;
					line_xxyy(10+unit_l*((sumN-j-1)*2+move_x), FF_y+move_y+unit_l*(times), and_x, FF_y+move_y+unit_l*(times));
					times = times + 1;
				}
			}
			and_h = 40*(times/2);
			AND(and_x, FF_y+move_y+unit_l*(times-1)/2-and_h/2, and_w, and_h);
			hh.push(FF_y+move_y+unit_l*(times-1)/2);
		}
		var avg = 0;
		for(i = 0; i < hh.length; i++){
			avg += hh[i];
		}
		avg = avg / hh.length;
		var or_w = 80;
		var or_h = 150*str.length/1.5;
		var FF_w = 150;
		var FF_h = 150;
		if(data.length / sumN > 1)
			OR(and_x+and_w+150, avg-or_h/2, or_w, or_h);
		else
			line_xxyy(and_x+and_w+150, avg, and_x+and_w+150+or_w+0.5*or_h, avg);
		line_xxyy(and_x+and_w+150+or_w+0.5*or_h, avg, FF_x-0.9*FF_w, avg);
		line_xxyy(FF_x-0.9*FF_w, avg, FF_x-0.9*FF_w, FF_y+u_d*0.3*FF_h);
	}

	function designOutput(output_exp){
		var web_h = $(document).height();
		var web_w = $(document).width();
		var unit = 20;
		var x = web_w - 200;
		for(i = 0; i < 2*sumN; i++){
			line_len(x + i*unit, 120, 0, 2710);
		}

		var i, j;
		var str = [];
		for(i = 0; i < output_exp.length/sumN; i++){
			var tmp_str = "";
			for(j = 0; j < sumN; j++){
				tmp_str += output_exp[i*sumN+j];
			}
			str.push(tmp_str);
		}   
		var FF_y = web_h;
		var and_w = 50;
		var and_h = 50*(times/2);
		var hh = [];
		var and_x = x + 200;
		for(i = 0; i < str.length; i++){
			var times = 0;
			var move_y = 70+150*i;
			for(j = 0; j < sumN; j++){
				if(parseInt(str[i][j]) != 2){
					var move_x = (parseInt(str[i][j]) == 1)? 0:1;
					var unit_l = 20;
					line_xxyy(x+unit_l*((sumN-j-1)*2+move_x), FF_y+move_y+unit_l*(times), and_x, FF_y+move_y+unit_l*(times));
					times = times + 1;
				}
			}
			and_h = 40*(times/2);
			AND(and_x, FF_y+move_y+unit_l*(times-1)/2-and_h/2, and_w, and_h);
			hh.push(FF_y+move_y+unit_l*(times-1)/2);
		}
		var avg = 0;
		for(i = 0; i < hh.length; i++){
			avg += hh[i];
		}
		avg = avg / hh.length;
		var or_w = 80;
		var or_h = 150*str.length/1.5;
		var FF_w = 150;
		var FF_h = 150;
		if(output_exp.length / sumN > 1)
			OR(and_x+and_w+150, avg-or_h/2, or_w, or_h);
		else
			line_xxyy(and_x+and_w+150, avg, and_x+and_w+150+or_w+0.5*or_h, avg);
		line_len(and_x+and_w+150+or_w+0.5*or_h, avg, 300, 0);
		ctx.font = "45px Consola";
		ctx.fillText('Z', and_x+and_w+150+or_w+0.5*or_h+300+10, avg+15);
	}
		

	function leftLine(){
		var web_h = $(document).height();
		var web_w = $(document).width();
		var input_x = 10;
		var unit = 20;
		var i;
		for(i = 1; i <= 2*sumN; i++){

			if(i <= 2*inputN && i % 2 == 1){
				ctx.font = "20px Consola";
				ctx.fillText('X'+(i+1)/2, input_x+(i-1)*unit-10, 40);
				line_len(input_x+(i-1)*unit, 120-40, 0, 2710+40);
			}
			else{
				line_len(input_x+(i-1)*unit, 120, 0, 2710);
			}
			if(i % 2 == 1){
				NOT(input_x+(i-1)*unit, 120-5*2.732, 21);
			}
			if(i == 1){
				line_len(input_x+(i-1)*unit, 120+2710, 0 , 25);
				line_xxyy(input_x+(i-1)*unit, 120+2710+25, web_w - 200, 120+2710+25);
				line_len(web_w - 200, 120+2710, 0 , 25);
			}
			else if(i == 2*sumN){
				line_len(input_x+(i-1)*unit, 120+2710, 0 , 35);
				line_xxyy(input_x+(i-1)*unit, 120+2710+35, web_w-200+(i-1)*unit, 120+2710+35);
				line_len(web_w-200+(i-1)*unit, 120+2710, 0 , 35);
			}
		}
	}

	function rightLine(){
		var i;
		var web_h = $(document).height();
		var web_w = $(document).width();
		var FF_x = web_w-500;
		var width = 150;
		var height = 150;
		var input_x = 10;
		var unit_r = 30;
		var unit_l = 20;

		for(i = 0; i < stateN; i++){
			var origin_y;
			if(stateN == 1){
				origin_y = web_h;
			}
			else if(stateN == 2){
				origin_y = ((i+1)/(stateN+1))*(web_h*2);
			}
			else if(stateN >= 3){
				origin_y = 300+(i/(stateN-1))*((web_h-100)*1.8);
			}
			var x = FF_x+0.9*width;
			var y = origin_y-0.3*height;
			line_len(x, y, i*unit_r, 0);
			line_xxyy(x+i*unit_r, y, x+i*unit_r, 30+(stateN-i-1)*0.5*unit_r);
			line_xxyy(x+i*unit_r, 30+(stateN-i-1)*0.5*unit_r, 10+unit_l*(2*inputN+2*(stateN-i-1)), 30+(stateN-i-1)*0.5*unit_r);
			line_xxyy(10+unit_l*(2*inputN+2*(stateN-i-1)), 30+(stateN-i-1)*0.5*unit_r, 10+unit_l*(2*inputN+2*(stateN-i-1)), 120);
		}

	}

	function line_len(x, y, width, height){
		ctx.moveTo(x, y);
		ctx.lineTo(x+width, y+height);
		ctx.stroke();
	}

	function line_xxyy(x, y, xx, yy){
		ctx.moveTo(x, y);
		ctx.lineTo(xx, yy);
		ctx.stroke();
	}

	function FF(type, centerX, centerY, width, height){
		x = centerX - 0.5*width;
		y = centerY - 0.5*height;
		var margin = 10;
		ctx.font = "24px Consola";
		ctx.rect(x, y, width, height);
		if(type == 1)
			ctx.fillText('D', x+margin, y+0.25*height);
		else if(type == 2)
			ctx.fillText('T', x+margin, y+0.25*height);
		else if(type == 3){
			ctx.fillText('J', x+margin, y+0.25*height);
			ctx.fillText('K', x+margin, y+0.85*height);
			line_len(x-0.4*width, y+0.8*height, 0.4*width, 0);
		}
		else if(type == 4){
			ctx.fillText('R', x+margin, y+0.25*height);
			ctx.fillText('S', x+margin, y+0.85*height);
			line_len(x-0.4*width, y+0.8*height, 0.4*width, 0);
		}

		ctx.fillText('Q', x+width-3*margin, y+0.25*height);
		ctx.fillText('FF', x+0.425*width, y+0.55*height);
		ctx.fillText('—', x+width-3.25*margin, y+0.75*height);
		ctx.fillText('Q', x+width-3*margin, y+0.85*height);

		// CLK
		if(type == 1 || type == 2){
			line_len(x, y+0.7*height, 0.2*width, 0.1*height);
			line_len(x+0.2*width, y+0.8*height, -0.2*width, 0.1*height);
		}
		else if(type ==3){
			line_len(x, y+0.4*height, 0.2*width, 0.1*height);
			line_len(x+0.2*width, y+0.5*height, -0.2*width, 0.1*height);
		}

		line_len(x+width, y+0.2*height, 0.4*width, 0);
		line_len(x, y+0.2*height, -0.4*width, 0);
	}

	// Gates and FFs
	function NOT(x, y, unit){
		line_len(x, y, 0.7*unit, 0);
		line_len(x+0.45*unit, y-1.732/4*unit, unit, 0);
		line_len(x+0.45*unit, y-1.732/4*unit, 0.5*unit, 1.732/2*unit);
		line_len(x+1.45*unit, y-1.732/4*unit, -0.5*unit, 1.732/2*unit);
		var radius = unit / 8;
		ctx.moveTo(x+0.95*unit+radius, y+1.732/4*unit+radius);
		ctx.arc(x+0.95*unit,y+1.732/4*unit+radius,radius,0,2*Math.PI);
		ctx.stroke();
	}

	function AND(x, y, width, height){
		line_len(x, y, width, 0);
		ctx.moveTo(x+width, y);
		ctx.arc(x+width, y+0.5*height, 0.5*height, 1.5*Math.PI, 0.5*Math.PI);
		line_len(x, y+height, width, 0);
		line_len(x, y, 0, height);
		line_len(x+width+0.5*height, y+0.5*height, 150-0.5*height, 0);
		ctx.stroke();
	}

	function OR(x, y, width, height){
		line_len(x, y, width, 0);
		ctx.moveTo(x+width, y);
		ctx.arc(x+width, y+0.5*height, 0.5*height,1.5*Math.PI,0.5*Math.PI);
		ctx.moveTo(x, y);
		ctx.quadraticCurveTo(x+width, y+0.5*height, x, y+height);
		line_len(x, y+height, width, 0);
		ctx.stroke();
	}

};

