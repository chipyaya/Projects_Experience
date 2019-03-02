window.fbAsyncInit = function(){
	FB.init({
		appId      : '970489853040863',
		cookie     : true,
		xfbml      : true,
		version    : 'v2.5'
	});
};

(function(d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) return;
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

var photourl="";
var access_token=""
function statusChangeCallback(response) {

	FB.login(function(response) {

		access_token = response.authResponse.accessToken;

		FB.api('/me', function(response) {
			var user_name = response.name;
			var user_id = response.id;

			$('#fbmessage').fadeIn();
			$('#fbmessage a').click(function(){	
				$.post('/uploadtofb',{token:access_token, message:$('#fbmessage textarea').val()},function(result){
					$('#fbmessage').hide();
					$('#fbmessage textarea').val("");
					$('.sharebtns a.button:nth-child(1)').text('上傳成功!');
					$('.sharebtns a.button:nth-child(1)').animate({'color':'#feb900'},100);
					$('.sharebtns a.button:nth-child(1)').animate({'border-color':'#feb900'},100);
					$('.sharebtns a.button:nth-child(1)').attr('onclick',"");
				});
			});

		});

	}, {scope: 'publish_actions'});    
}


function checkLoginState() {				//call by the button "login Fb and upload img" 
	FB.getLoginStatus(function(response) {
		$.post('/openosk');
		statusChangeCallback(response);		//upload img to fb
	});

}


function restart(){  
	if(access_token != "")                       //call by the button "END"
		FB.logout(function(response) {});       //logout FB account
	$.get('/clean',function(data){
		window.location.href='/';
	});
}


function uploadtofb(){
	checkLoginState();
}


function uploadtoimgur(){

	$('#loading').css('display','block');		//display "loading" animation
	$('.content').css('display','none');		//hide Q14 content
	$.get('/uploadtoimgur',function(result){	//go to app.js
		window.location.href='/share';			//go to /share
	});
}


function makeqrcode(){							//Call by the button "QRcode and download img"
	$.get('/makeqrcode',function(data){
		$('.qrcode').attr('src','makeqrcode');
		$('a.qrcodebutton').animate({height:200},1000);
		$('#whitebg').show();
	});
}




