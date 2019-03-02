(function(){
	var loadDiv = document.getElementById("load");
	var imgDiv = document.getElementById("result");
	var show = function(){
		imgDiv.style.display = "none";
		loadDiv.style.display = "block";
		setTimeout(hide, 4300);  // 4300 mini-seconds
	}

	var hide = function(){
		loadDiv.style.display = "none";
		imgDiv.style.display = "block";
	}
	show();
})();
