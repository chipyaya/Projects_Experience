var composite = function(){
	exec('./processImg/commands', function(err, data) {  
		console.log(err)
		console.log(data.toString());                       
	});  
}

