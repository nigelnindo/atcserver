var pictureSource;
var destinationType;

$(document).ready(function(){
	$('#take-picture').click(function(e){
		console.log('capture photo clicked.');
		capturePhoto();
	});
});

document.addEventListener("deviceready",onDeviceReady,false);

function onDeviceReady() {
		console.log('Device is ready');
        pictureSource=navigator.camera.PictureSourceType;
        destinationType=navigator.camera.DestinationType;
}

function capturePhoto() {
      // Take picture using device camera and retrieve image as file uri
      console.log('Trying to capture photo.');
      navigator.camera.getPicture(onPhotoDataSuccess, onFail, { quality: 50,
        destinationType: destinationType.FILE_URI,
        saveToPhotoAlbum:true});
}

function onPhotoDataSuccess(imageData){
    console.log('onPhotoDataSuccess: Method Invoked.');
    console.log('imageData: '+imageData);
    var proPic = localStorage.setItem("proPic",imageData);
	 
    var newHtml = '<img style="width:100%;" id="my-profile-pic" src='+localStorage.getItem('proPic')+'>';

    document.getElementById('image-holder').innerHTML = newHtml;

    console.log(document.getElementById('login-img-container').innerHTML);

    //var myImageView = document.getElementById('my-profile-pic'); 
  	//myImageView.style.display = 'block';
    //imageView.src =  + imageData;
    
	  console.log('onPhotoDataSuccess: Method Finished.');
}

function onFail(message){
	console.log('onFail called.');
	alert('Failed because: '+message);
}










