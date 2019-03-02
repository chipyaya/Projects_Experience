$.post('/ratio', function(data){
	var win_ratio = parseInt(data.ratio);
	draw(win_ratio);
	display(win_ratio);
});

function draw(win_ratio) {
	var loo_ratio = 100 - win_ratio;
	$('#pie').highcharts({
		chart: {
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
			type: 'pie',
		},
		title: {
			text: ''
		},
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				innerSize: '60%',
				dataLabels: {
					enabled: true,
					distance: -90,
					formatter: function() {
						if(this.percentage!=0)  
							return Math.round(this.percentage)  + '%';
					},
					style:{
						fontFamily: 'Consolas',
						fontSize: '40px'
					}
				}
			},
		},
		series: [{
			name: '比例',
			colorByPoint: true,
			data: [{
				name: 'winner',
				color: '#A5F0B8',
				y: win_ratio			//??
				
			}, {
				name: 'loser',
				color: '#84D1F0',
				y: loo_ratio			//??
			}]
		}]
	});
}


function display(win_ratio) {
	var win = document.getElementById('win_ratio'); 
	win.innerHTML = win_ratio; //display output in DOM
	var loo = document.getElementById('loo_ratio'); 
	loo.innerHTML = 100-win_ratio; //display output in DOM
}

/*
$.post('/ratio', function(win_ratio){
});
*/
