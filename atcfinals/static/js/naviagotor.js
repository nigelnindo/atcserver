$(document).ready(function(){
       $("#go_to_signup").click(function(e){
            e.preventDefault();
            $.mobile.changePage("index.html#signup_page",{transition:'slidedown'});
       });
    
       $("#signup_landing").click(function(e){
            e.preventDefault();
            $.mobile.changePage("index.html#landing_page",{transition:'slideup'});   
       });    
    
       $("#go_to_login").click(function(e){
        e.preventDefault();
           $.mobile.changePage("index.html#camera_page",{transiton:'slidedown'});
       });

       $("#go-explore").click(function(e){
          e.preventDefault();
          $.mobile.changePage("index.html#users_page",{transition:'slideup'});
       });
        
       $('ul li.my-user-list-item').click(function(e){
          e.preventDefault();
          console.log('user list item clciked.');
       });

});

$(document).on('on-refresh-comments',function(){
    console.log('On refresh comments event invoked');
     $('#my-comment-list li').on('click', function(){
        console.log('List item clicked');
     });
});

/*
$( document ).on( "pageinit", "#submit-page", function() {
    console.log('Google maps function running')
    var defaultLatLng = new google.maps.LatLng(34.0983425, -118.3267434);  // Default to Hollywood, CA when no geolocation support
    if ( navigator.geolocation ) {
        function success(pos) {
            // Location found, show map with these coordinates
            drawMap(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude));
        }
        function fail(error) {
            drawMap(defaultLatLng);  // Failed to find location, show default map
        }
        // Find the users current position.  Cache the location for 5 minutes, timeout after 6 seconds
        navigator.geolocation.getCurrentPosition(success, fail, {maximumAge: 500000, enableHighAccuracy:true, timeout: 6000});
    } else {
        drawMap(defaultLatLng);  // No geolocation support, show default map
    }
    function drawMap(latlng) {
        var myOptions = {
            zoom: 10,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
        // Add an overlay to the map of current lat/lng
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            title: "Greetings!"
        });
    }
});
*/