$("#landing_page").on("pagebeforeshow",function(e){
        console.log('pagebeforeshow triggered');
    });

$(document).ready(function(){

    var tryToken = function(){
        $.ajax({
            type:'GET',
            url:'http://127.0.0.1:8000/trytoken/',
            headers:{
                'Authorization':'Token '+localStorage.getItem('token')
            },
            success: function(data){
                new $.nd2Toast({
                    message : data,
                    ttl : 3000
                });   
            },
            error: function(){
                new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });
            }
        });
    };
    
    $('#try-token').click(function(event) {
        tryToken();
    });

    var getToken = function(){
        $.ajax({
        type:'POST',
        url: 'http://127.0.0.1:8000/api-token-auth/',
        data: {
            username: "nigel",
            password: "niglexia.100"
        },
        success: function(responseData,status){
             new $.nd2Toast({
                    message : responseData.token,
                    ttl : 3000
                });
            localStorage.setItem('token',responseData.token);
        },
        error: function(){
             new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });
        }
    });
    };

    $('#get-token').click(function(event) {
        getToken();
    });

    var loadReports = function(data){
        data.forEach(function(report){

            $('ul#my-user-list').append('<li class="my-user-list-item"><a href="#"><img src="img/user.png" class="ui-thumbnail ui-thumbnail-circular"/><h2>'+report.id_number+'</h2><p>'+report.description+'</p></a></li>');            
                
        });
        
    $("ul#my-user-list").listview('refresh');
        
    };

    var getReports = function(){
        $.ajax({
            type:'GET',
            url:'http://atcserver.herokuapp.com/reports',
            success: function(data,status){
                console.log(data);
                loadReports(data);
            },
            error: function(xhr,status){
                console.log('Request failed.');
                new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });

            }
        });
    };  

    //https://dl-web.dropbox.com/get/Apps/ATCAPI/testImages/zbzie1438763770961.jpg
    //https://dl.dropboxusercontent.com/s/kyjm1pr79g2irfj/Guinness%20Storehouse%20top.jpg
    $("#incidents-page").on('pagebeforeshow',function(e){

        console.log("Incidents Page showing.");

        $('ul#my-user-list').empty();
        getReports();

        
    });


    $('#submit-page').on('pagebeforeshow',function(e){
        if(navigator.geolocation){
            console.log('geolocation available');
            function success(pos){
                console.log('location detected');
                alert('Location detected.');
            }
            function fail(error){
                console.log('unable to detect location');
                alert('Unable to detect your location.');
            }
            navigator.geolocation.getCurrentPosition(success,fail,{maximumAge: 500000, enableHighAccuracy:true, timeout: 6000});
        }
        else{
            console.log('geolocation not available');
            alert('Unable to detect your location.');
        }

        var mapProp = {
    center:new google.maps.LatLng(51.508742,-0.120850),
    zoom:5,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("map-canvas"),mapProp);

        
    });

    var sendImage = function(){
        var sendImageSuccess = function(){
            console.log('sent to server!');
            alert("Image sent successfully!");
        };

        var sendImageFail = function(e){

    alert('\ncode:'+e.code+'\nstatus:'+e.http_status+'\nexception'+e.exception+'\nbody:'+e.body+'\nsource:'+e.source);
            
        console.log('upload failed');
            
        };

        var fromURI = localStorage.getItem('proPic');
        
        var toURI = "http://atcserver.herokuapp.com/reports/upload/";
        var options = new FileUploadOptions();
        
        options.fileKey = 'reportedImage';
        options.fileName = fromURI.substr(fromURI.lastIndexOf('/')+1);
        options.mimeType = "image/jpeg";
        options.params = {
            id_number: $('#idnum').val(),
            description: $('#desc').val(),
            latitude: "No latitude data for now",
            longitude: "No longitude data for now"
        };

        var ft = new FileTransfer();
        ft.upload(fromURI,encodeURI(toURI),sendImageSuccess,sendImageFail,options);
    
    };

    $('#send-to-server').click(function(event) {
        console.log('Click event to send image invoked.');
        sendImage();
    });


    var getCommentsList = function(){
        $.ajax({
            type:'GET',
            url:'http://127.0.0.1:8000/comments',
            success: function(data,status){
                console.log(data);
                loadComments(data);
            },
            error: function(xhr,status){
                console.log('Request failed.');
                new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });

            }
        });
    };

    var loadComments = function(data){
        $('ul#my-comment-list').empty();

        data.forEach(function(comment){
            $('ul#my-comment-list').append('<li><a href="#"><h2>'+comment.comment_text+'</h2><p>'+comment.user_relation.username+'</p><h2>'+comment.question_relation.question_text+'</h2></a></li>');            
        });
        
        console.log('before append');
        $('ul#my-comment-list').append('<li id="click-tester"><a href="#"><h2>Comment Text</h2><p>Username</p><h2>Question Text</h2></a></li>');
        console.log('after append');

        $(document).trigger('on-refresh-comments');

        $('ul#my-comment-list').listview('refresh');
    };

    $(document).on('pagebeforeshow','#comments_page',function(){
        console.log('questions page has been opened.');
        getCommentsList();
    });


    var getQuestionsList = function(){
        $.ajax({
            type:'GET',
            url:'http://127.0.0.1:8000/questions',
            success: function(data,status){
                console.log(data);
                loadQuestions(data);
            },
            error: function(xhr,status){
                console.log('Request failed.');
                new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });

            }
        });
    };

    var loadQuestions= function(data){
        $('ul#my-question-list').empty();
        data.forEach(function(question){
            $('ul#my-question-list').append('<li><a href="#"><h2>'+question.question_text+'</h2></a></li>');
        });
        $('ul#my-question-list').listview('refresh');
    };


    $(document).on('pagebeforeshow','#questions_page',function(){
        console.log('quetsions page has been opened.');
        getQuestionsList();
    });


    var getUserList = function(){
        $.ajax({
            type:'GET',
            url:'http://127.0.0.1:8000/userprofiles',
            success: function(data,status){
                console.log(data);
                loadUsers(data);
            },
            error: function(xhr,status){
                console.log('Request failed.');
                new $.nd2Toast({
                    message : "Server returned an error message.",
                    ttl : 3000
                });

            }
        });
    };

    var loadUsers = function(data){
        $('ul#my-user-list').empty();

        data.forEach(function(user){
            
            $('ul#my-user-list').append('<li class="my-user-list-item"><a href="#"><img src="img/user.png" class="ui-thumbnail ui-thumbnail-circular"/><h2>'+user.user_relation.username+'</h2><p>'+user.description+'</p></a></li>');            
        
        });

        $("ul#my-user-list").listview('refresh');
    };


    //call page before show event to load data
    $(document).on('pagebeforeshow','#users_page',function(){
        console.log('users page has been opened.');
        getUserList();
    });


    //nativedroid2 toast
    /*
    new $.nd2Toast({
                    message : "Message has been deleted",
                    action : {
                        title : "undo",
                        fn : function() {
                            console.log("I am the function called by 'Pick phone...'");
                        },
                        color : "lime"
                    },
                    ttl : 3000
                });
    */

    var trysession = function(){
        sessionStorage.setItem("username","nigel");
        console.log('username: '+sessionStorage.getItem("username"));
    };

    trysession();

    var changeSession = function(){
        sessionStorage.setItem("username","nigelnindo");
        console.log('username: '+sessionStorage.getItem('username'));
    };

    changeSession();

    //get all posts from the database
    var getData = function(){
        $.ajax({
            type:'GET',
            url:'http://127.0.0.1:8000/posts',
            success: function(data,status){
                console.log(data);
                populateListUi(data);
            },
            error: function(xhr,status){
                console.log('Request failed.');
            }
        });
    };

    getData();

    var populateListUi = function(data){
        data.forEach(function(innovation){
            console.log(innovation.innovation_name);
            $("ul#my-list").append('<li><a href="#"><h2>'+innovation.innovation_name+'</h2><p>'+innovation.innovation_creator.relation.username+'</p></a></li>');
            $("ul#my-list").listview('refresh');
            console.log('List populated');
        });
    };

    $("#signup_request").click(function(){
        var details = {
            username: null,
            password: null,
            gender: null,
            description: null
        };
        
        details.username = $("#username_input").val();
        details.password = $("#password_input").val();
        details.gender = $("#select-gender option:selected").text();
        details.description = $("#describe_yourself").val();
        
        console.log(details);
        
        if(details.gender == 'Male'){
            details.gender = 'male';
        }
        else{
            details.gender = 'female';
        }
        
        json_data = JSON.stringify(details);
        console.log(json_data);
        
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/signup/',
            data:details,
            success: function(){
                console.log('Request successful!');
                new $.nd2Toast({
                    message : "Sign Up successful",
                    ttl : 3000
                });
            },
            error: function(responseData,textStatus){
                console.log('Request Failed');
                console.log(textStatus.toString());
                new $.nd2Toast({
                    message : "Sign Up  unsuccessful",
                    ttl : 3000
                });
            }
        });
        
    });   
});